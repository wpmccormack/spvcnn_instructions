# spvcnn_instructions

## Code Setup

To set up cmssw with spvcnn, please do the following standard command

```
source /cvmfs/cms.cern.ch/cmsset_default.sh
```
Then go to a directory where you want to work and do
```
cmsrel CMSSW_13_3_0_pre5
cd CMSSW_13_3_0_pre5/src/
cmsenv
git cms-init
git cms-merge-topic wpmccormack:add_spvcnn
git clone git@github.com:AlexSchuy/python_backend.git RecoParticleFlow/PFClusterProducer/data
scram b -j 4
```

There are a couple important things to note here
1. For step2 (HLT) workflows, you should use HLTrigger/Configuration/python/HLT_GRun_SONIC_cff.py, which contains fragment.hltParticleFlowRecHitHBHESPVCNN and a modified version of fragment.hltParticleFlowClusterHCAL to use the new SONIC producer for SPVCNN.  It also adds the fragment.hltParticleFlowRecHitHBHESPVCNN component to several workflows in the bottom of the cff file.  This is important!
2. For step 3 workflows, there is a new RecoParticleFlow/PFClusterProducer/python/particleFlowClusterHCAL_cfi.py, which runs SPVCNN through the new SONIC poducer.  The original version of HCAL clustering is in particleFlowClusterHCAL_original_cfi.py.  If you change the name of particleFlowClusterHCAL_original_cfi.py to particleFlowClusterHCAL_cfi.py, then the workflow will use use the default clustering rather than SPVCNN (you might want to stash the SONIC producer version somewhere though).
3. In the SPVCNN config files referenced above, the model is named spvcnn_td_7_tbeta_10.  You might have to change that depending on how you choose to name the model

In your job configs, you need to add a few lines.
```
from Configuration.ProcessModifiers.enableSonicTriton_cff import enableSonicTriton
```
and
```
process.load("HeterogeneousCore.SonicTriton.TritonService_cff")
allSonicTriton = cms.ModifierChain(enableSonicTriton)
```
Also, just as a reminder, if there's a line like
```
process.load('HLTrigger.Configuration.HLT_GRun_cff')
```
in your run config, then you should change that to
```
process.load('HLTrigger.Configuration.HLT_GRun_SONIC_cff')
```
Alternatively, you can just copy the fragments I mentioned in 1 above into whatever cff file you are using that contains the particleFlow producers and modifications to the workflows.

And you need to add something like
```
process.TritonService.verbose = True
process.TritonService.fallback.verbose = True
process.TritonService.fallback.useDocker = False
process.TritonService.fallback.useGPU = False
process.TritonService.servers.append(
    cms.PSet(
        name = cms.untracked.string("default"),
        address = cms.untracked.string("ailab01.fnal.gov"),
        port = cms.untracked.uint32(8071),
        useSsl = cms.untracked.bool(False),
        rootCertificates = cms.untracked.string(""),
        privateKey = cms.untracked.string(""),
        certificateChain = cms.untracked.string(""),
    )
)
```
You'll need to point the address to whereever you have your server set up, and change the port accordingly too.


## Server setup

First, make some working directory.  Then run
```
git clone git@github.com:mit-han-lab/spvnas-dev.git
cd spvnas-dev/
git checkout 13dd8ffe979f934436d19fdf1075be5511098c08
cd ..
git clone git@github.com:AlexSchuy/python_backend.git
docker build -f python_backend/Dockerfile . -t triton-spvcnn
```