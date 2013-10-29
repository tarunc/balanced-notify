#
# Cookbook Name:: notify
# Recipe:: default
#
# Copyright (C) 2013 Mahmoud Abdelkader
#
# All rights reserved - Do Not Redistribute
#

# install dependencies

include_recipe 'apt'

Chef::Log.info 'Refreshing the cache-yo'
execute 'apt-get-update-periodic' do
  command 'apt-get update'
  ignore_failure true
  only_if do
   ::File.exists?('/var/lib/apt/periodic/update-success-stamp') &&
   ::File.mtime('/var/lib/apt/periodic/update-success-stamp') < Time.now - 86400
  end
end

include_recipe 'python'
include_recipe 'python::pip'
include_recipe 'python::virtualenv'

include_recipe 'mongodb::10gen_repo'
include_recipe 'mongodb'

# install python stuff

venv_directory = '/home/vagrant'

python_virtualenv "#{venv_directory}/.virtualenvs/notify" do
    interpreter 'python2.7'
    owner 'vagrant'
    group 'vagrant'
    action :create
end

python_pip 'install-requirements' do
  options '-r'
  package_name "/home/vagrant/notify/requirements.txt"
  virtualenv "/home/vagrant/.virtualenvs/notify"
  action :install
end

execute 'notify[python-setup.py-develop]' do
  cwd '/home/vagrant/notify'
  command <<-EOH
  #{venv_directory}/.virtualenvs/notify/bin/python setup.py develop
  EOH
end