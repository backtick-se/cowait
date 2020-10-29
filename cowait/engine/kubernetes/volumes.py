from kubernetes import client


VOLUME_SOURCES = {
    'aws_elastic_block_store': client.V1AWSElasticBlockStoreVolumeSource,
    'azure_disk': client.V1AzureDiskVolumeSource,
    'azure_file': client.V1AzureFileVolumeSource,
    'cephfs': client.V1CephFSVolumeSource,
    'cinder': client.V1CinderVolumeSource,
    'config_map': client.V1ConfigMapVolumeSource,
    'csi': client.V1CSIVolumeSource,
    'downward_api': client.V1DownwardAPIVolumeSource,
    'empty_dir': client.V1EmptyDirVolumeSource,
    'fc': client.V1FCVolumeSource,
    'flex_volume': client.V1FlexVolumeSource,
    'flocker': client.V1FlockerVolumeSource,
    'gce_persistent_disk': client.V1GCEPersistentDiskVolumeSource,
    'git_repo': client.V1GitRepoVolumeSource,
    'glusterfs': client.V1GlusterfsVolumeSource,
    'host_path': client.V1HostPathVolumeSource,
    'iscsi': client.V1ISCSIVolumeSource,
    'nfs': client.V1NFSVolumeSource,
    'persistent_volume_claim': client.V1PersistentVolumeClaimVolumeSource,
    'photon_persistent_disk': client.V1PhotonPersistentDiskVolumeSource,
    'portworx_volume': client.V1PortworxVolumeSource,
    'projected': client.V1ProjectedVolumeSource,
    'quobyte': client.V1QuobyteVolumeSource,
    'rbd': client.V1RBDVolumeSource,
    'scale_io': client.V1ScaleIOVolumeSource,
    'secret': client.V1SecretVolumeSource,
    'storageos': client.V1StorageOSVolumeSource,
    'vsphere_volume': client.V1VsphereVirtualDiskVolumeSource,
}


def create_volumes(task_volumes):
    index = 0
    mounts = []
    volumes = []
    for target, volume in task_volumes.items():
        index += 1
        name = volume.get('name', f'volume{index}')
        for source_type, VolumeSource in VOLUME_SOURCES.items():
            if source_type not in volume:
                continue

            volume_config = volume[source_type]
            volumes.append(client.V1Volume(**{
                'name': name,
                source_type: VolumeSource(**volume_config),
            }))
            mounts.append(client.V1VolumeMount(
                name=name,
                read_only=volume.get('read_only', False),
                mount_path=target,
            ))

    return volumes, mounts
