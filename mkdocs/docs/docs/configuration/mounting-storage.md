---
Title: Mounting the External Storage
Description: Storage
Sort: 1
---

You can mount your storage device at a specific folder location. It is conventional to do this within the `/mnt` folder, for example `/mnt/storage`. Note that the folder must be empty.

Plug the storage device into a USB port on the Raspberry Pi.

List all the disk partitions on the Raspberry Pi using the following command:

```bash
     sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL
```

You should get an output like this:

```
UUID                                 NAME        FSTYPE    SIZE MOUNTPOINT       LABEL   MODEL
                                     loop0       squashfs 84.4M /snap/core/11321
                                     sda                   5.5T                          Expansion_Desk
67E3-17ED                            ├─sda1      vfat      200M                  EFI
6088-A250                            └─sda2      exfat     5.5T                  storage
                                     mmcblk0              29.7G
7581-8A48                            ├─mmcblk0p1 vfat      256M /boot            boot
fa37d505-e741-4d35-bcec-4580aef395e1 └─mmcblk0p2 ext4     29.5G /                rootfs
```

The Raspberry Pi uses mount points `/` and `/boot`. Your storage device will show up in this list, along with any other connected storage.

Use the SIZE, LABEL, and MODEL columns to identify the name of the disk partition that points to your storage device. For example, sda1.

The FSTYPE column contains the filesystem type. If your storage device uses an exFAT file system, install the exFAT driver:

```
sudo apt update
sudo apt install exfat-fuse
```

If your storage device uses an NTFS file system, you will have read-only access to it. If you want to write to the device, you can install the ntfs-3g driver:

```
sudo apt update
sudo apt install ntfs-3g
```

Run the following command to get the location of the disk partition:

```
sudo blkid
```

For example, `/dev/sda1`.

Create a target folder to be the mount point of the storage device. The mount point name used in this case is `storage`. You can specify a name of your choice:

```
sudo mkdir /mnt/storage
```

Mount the storage device at the mount point you created:

```
sudo mount /dev/sda1 /mnt/storage
```

Verify that the storage device is mounted successfully by listing the contents:

```
ls /mnt/storage
```

## Setting up Automatic Mounting

You can modify the fstab file to define the location where the storage device will be automatically mounted when the Raspberry Pi starts up. In the fstab file, the disk partition is identified by the universally unique identifier (UUID).

Get the UUID of the disk partition:

```
sudo blkid
```

Find the disk partition from the list and note the UUID. For example, 5C24-1453.

Open the fstab file using a command line editor such as nano:

```
sudo nano /etc/fstab
```

Add the following line in the fstab file:

```
UUID=6088-A250 /mnt/storage fstype users,defaults,uid=1000,gid=1000,umask=0022,auto,rw,nofail,umask=000,x-systemd.device-timeout=30 0 0
```

Replace fstype with the type of your file system, for example: exfat.

If the filesystem type is FAT or NTFS, add ,umask=000 immediately after nofail - this will allow all users full read/write access to every file on the storage device.

---

This page was taken from the [Official Documentation](https://www.raspberrypi.com/documentation/computers/configuration.html#mounting-a-storage-device), please refer to it for more information.
