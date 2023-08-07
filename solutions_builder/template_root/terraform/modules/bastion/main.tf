module "iap_bastion" {
  source                     = "terraform-google-modules/bastion-host/google"
  version                    = "5.3.0"
  name                       = "jump-host"
  machine_type               = var.machine_type
  project                    = var.project_id
  zone                       = var.zone
  network                    = var.vpc_network_self_link
  subnet                     = var.vpc_subnetworks_self_link
  image                      = var.image
  image_family               = var.image_family
  image_project              = var.image_project
  disk_size_gb               = var.disk_size_gb
  disk_type                  = "pd-balanced"
  fw_name_allow_ssh_from_iap = "allow-ssh-ingress-from-iap"
  startup_script             = var.startup_script
}
