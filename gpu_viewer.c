#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/pci.h>

#define PROC_NAME "gpu_viewer"

static int show_gpus(struct seq_file *m, void *v) {
    struct pci_dev *dev = NULL;

    for_each_pci_dev(dev) {
        if ((dev->class >> 8) == PCI_CLASS_DISPLAY_VGA ||
            (dev->class >> 8) == PCI_CLASS_DISPLAY_3D) {

            seq_printf(m, "Vendor ID: 0x%04x\n", dev->vendor);
            seq_printf(m, "Device ID: 0x%04x\n", dev->device);
            seq_printf(m, "Bus: %02x:%02x.%d\n", dev->bus->number, PCI_SLOT(dev->devfn), PCI_FUNC(dev->devfn));
            seq_printf(m, "IRQ: %d\n", dev->irq);
            seq_printf(m, "Driver: %s\n", dev->driver ? dev->driver->name : "Unknown");
            seq_printf(m, "PCI Class: 0x%06x\n\n", dev->class);
        }
    }
    return 0;
}

static int open_proc(struct inode *inode, struct file *file) {
    return single_open(file, show_gpus, NULL);
}

static const struct file_operations proc_fops = {
    .owner = THIS_MODULE,
    .open = open_proc,
    .read = seq_read,
    .llseek = seq_lseek,
    .release = single_release,
};

static int __init gpu_viewer_init(void) {
    proc_create(PROC_NAME, 0, NULL, &proc_fops);
    printk(KERN_INFO "[gpu_viewer] module loaded\n");
    return 0;
}

static void __exit gpu_viewer_exit(void) {
    remove_proc_entry(PROC_NAME, NULL);
    printk(KERN_INFO "[gpu_viewer] module removed\n");
}

module_init(gpu_viewer_init);
module_exit(gpu_viewer_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("GPU Info Viewer");
MODULE_AUTHOR("You");
