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
git checkout 13dd8ff
cd ..
git clone git@github.com:wpmccormack/python_backend.git
cd python_backend
git checkout add_uproot
cd ..
docker build -f python_backend/Dockerfile . -t triton-spvcnn
```

Now we need to set up the model directories for SONIC.
The model file is included in my lpc eos directory.  Get it with
```
xrdcp -s root://cmseos.fnal.gov//store/user/wmccorma/spvcnn_checkpoint_Feb14_PFtarget_generic_WITHPU.pt .
```
You also need a yaml file with various model configurations.
Two important variables here are the td and tbeta values which hits can be used as condensation points and cluster radius.
If you use the macro writeYAMLs_Feb14_PFtarget_generic_WITHPU.py, you can automatically create yaml files for different td and tbeta values, and put them in a directory called yaml_files_Feb14_PFtarget_generic_WITHPU, which you need to make.  I haven't automated this - you can choose an alternate name or whatever you like, just modify the macro as appropriate.  You can also modify the yaml template by hand if you like.

The spvcnn default uses td of 0.7 and tbeta of 0.1.  I've explicitly included such a yaml file here as well: spvcnn_config_td_7_tbeta_10_ttbar.yaml.

You also need to set up the model files in the correct configuration for SONIC.


To be explicit, please go to the directory where you did the setup detailed above and do something like:
```
xrdcp -s root://cmseos.fnal.gov//store/user/wmccorma/spvcnn_checkpoint_Feb14_PFtarget_generic_WITHPU.pt .
wget https://raw.githubusercontent.com/wpmccormack/spvcnn_instructions/main/spvcnn_config_Feb14_PFtarget_generic_WITHPU_TEMPLATE.yaml
wget https://raw.githubusercontent.com/wpmccormack/spvcnn_instructions/main/writeYAMLs_Feb14_PFtarget_generic_WITHPU.py
mkdir yaml_files_Feb14_PFtarget_generic_WITHPU
python writeYAMLs_Feb14_PFtarget_generic_WITHPU.py
cd python_backend
mkdir spvcnn_TEMPLATE_Feb14_PFtarget_generic_WITHPU
cd spvcnn_TEMPLATE_Feb14_PFtarget_generic_WITHPU
mkdir 1
wget https://raw.githubusercontent.com/wpmccormack/spvcnn_instructions/main/spvcnn_TEMPLATE_Feb14_PFtarget_generic_WITHPU/config.pbtxt
cd 1
wget https://raw.githubusercontent.com/wpmccormack/spvcnn_instructions/main/spvcnn_TEMPLATE_Feb14_PFtarget_generic_WITHPU/1/model.py
cd ../../
mkdir oldmodels
cd models
mv spvcnn ../oldmodels/
wget https://raw.githubusercontent.com/wpmccormack/spvcnn_instructions/main/writeModels_Feb14_PFtarget_generic_WITHPU.py
python writeModels_Feb14_PFtarget_generic_WITHPU.py
cd ../../
```

(We move the older spvcnn directory because it has an old format)

Also, this is pretty ugly with all of the wgets.  Feel free to clone this directory somewhere and then copy files/directories into the appropriate places per the above instructions.

You can then start your server with something like
```
docker run --gpus all --shm-size=1g --ulimit memlock=-1  -p 8070:8000 -p 8071:8001 -p 8072:8002 --ulimit stack=67108864 -v$PWD:/code -ti triton-spvcnn
```
and
```
tritonserver --model-repository /code/python_backend/models
```
within the server.  Or all at once:
```
docker run --gpus all --shm-size=1g --ulimit memlock=-1  -p 8070:8000 -p 8071:8001 -p 8072:8002 --ulimit stack=67108864 -v$PWD:/code -ti triton-spvcnn tritonserver --model-repository /code/python_backend/models
```