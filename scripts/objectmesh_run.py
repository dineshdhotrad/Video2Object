import sys
from scripts.utils import mkdir, whereis
import subprocess
import os

def objectmesh(object_dir, frames_dir, focal, preset):
    if sys.platform.startswith('win'):
        cmd = "where"
        OPENMVG_BIN = "scripts/WinLibs/OpenMVG"
        OPENMVS_BIN = "scripts/WinLibs/OpenMVS"
    else:
        OPENMVG_BIN = whereis("openMVG_main_SfMInit_ImageListing")
        OPENMVG_BIN = "/opt/openmvg/bin"
        OPENMVS_BIN = whereis("ReconstructMesh")
        OPENMVS_BIN = "/opt/openmvs/bin/OpenMVS"
        
    output_dir = "reconstruction"
    print("Using input frame_dir  : ")
    print(object_dir + frames_dir)
    print("            output_dir : ")
    print(object_dir + output_dir)

    reconstruction_dir = os.path.join(object_dir + os.sep + output_dir, "sfm")
    matches_dir = os.path.join(reconstruction_dir, "matches")
    mvs_dir = os.path.join(object_dir + os.sep + output_dir, "mvs")

    mkdir(object_dir + os.sep + output_dir)
    mkdir(reconstruction_dir)
    mkdir(matches_dir)
    mkdir(mvs_dir)

    try:
        pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", frames_dir , "-o", matches_dir, "-f", focal])
        pIntrisics.wait()
        if pIntrisics.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Computing Intrensics")
        raise

    print("Compute features")
    try:
        pFeatures = subprocess.Popen( [os.path.join(OPENMVG_BIN, "openMVG_main_ComputeFeatures"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-m", "SIFT", "-p", preset] )
        pFeatures.wait()
        if pFeatures.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Compute features")
        raise

    print("Pair Generator in process")
    try:
        pMatches = subprocess.Popen( [os.path.join(OPENMVG_BIN, "openMVG_main_PairGenerator"), "-i", matches_dir+"/sfm_data.json", "-o", matches_dir+"/pairs.bin"] )
        pMatches.wait()
        if pMatches.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Compute Matches")
        raise
    
    print("Compute matches")
    print(os.path.join(OPENMVG_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-p", matches_dir+"/pairs.bin", "-o", matches_dir)
    try:
        pMatches = subprocess.Popen( [os.path.join(OPENMVG_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-p", matches_dir+"/pairs.bin","-o", matches_dir+"\matches.putative.bin", "-n", "HNSWL2"] )
        pMatches.wait()
        if pMatches.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Compute Matches")
        raise
    
    print("Filter matches")
    try:
        pMatches = subprocess.Popen( [os.path.join(OPENMVG_BIN, "openMVG_main_GeometricFilter"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir+"/matches.putative.bin", "-o", matches_dir+"/matches.f.bin"] )
        pMatches.wait()
        if pMatches.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Filter matches")
        raise

    print("Performing Sequential/Incremental reconstruction")
    try:
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_BIN, "openMVG_main_SfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir, "-s", "INCREMENTAL"] )
        pRecons.wait()
        if pRecons.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Compute features")
        raise
    
    print("Saving The Odometry/Extrensics")
    try:
        pInsave = subprocess.Popen( [os.path.join(OPENMVG_BIN, "openMVG_main_ConvertSfM_DataFormat"), "binary",  "-i", reconstruction_dir+"/sfm_data.bin", "-o", reconstruction_dir+"/sfm-data.json", "-V", "-I", "-E"] )
        pInsave.wait()
        if pInsave.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Saving The Odometry/Extrensics")
        raise

    print("Export to OpenMVS")
    try:
        pExpo = subprocess.Popen( [os.path.join(OPENMVG_BIN, "openMVG_main_openMVG2openMVS"), "-i", reconstruction_dir+"/sfm_data.bin", "-o", mvs_dir+"/scene.mvs", "-d", mvs_dir+"/images"] )
        pExpo.wait()

        if pExpo.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Export to OpenMVS")
        raise

    print("Densify point cloud")
    try:
        pDensify = subprocess.Popen( [os.path.join(OPENMVS_BIN, "DensifyPointCloud"), "scene.mvs" , "--dense-config-file", "Densify.ini", "--resolution-level", "1", "-w", mvs_dir] )
        pDensify.wait()
        if pDensify.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Densify point cloud")
        raise
    
    print("Reconstruct the mesh")
    try:
        pRemesh = subprocess.Popen( [os.path.join(OPENMVS_BIN, "ReconstructMesh"), "scene_dense.mvs" , "-w", mvs_dir] )
        pRemesh.wait()
        if pMatches.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Reconstruct the mesh")
        raise
    
    print("Refine the Mesh")
    try:
        pRefine = subprocess.Popen( [os.path.join(OPENMVS_BIN, "RefineMesh"), "scene_dense_mesh.mvs" , "--scales", "1", "-w", mvs_dir] )
        pRefine.wait()
        if pMatches.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Error Refine the Mesh")
        raise
    
    print("Texture the mesh and export final mesh with texture")
    try:
        pTexture = subprocess.Popen( [os.path.join(OPENMVS_BIN, "TextureMesh"), "scene_dense_mesh_refine.mvs" , "--decimate", "0.5", "-w", mvs_dir, "--export-type", "ply"] )
        pTexture.wait()
        if pMatches.returncode != 0:
            raise NameError("Mesh")
    except:
        print("Texture the mesh and export final mesh with texture")
        raise
    
    return True