#
# Cookbook Name:: notify
# Recipe:: default
#
# Copyright (C) 2013 Mahmoud Abdelkader
#
# All rights reserved - Do Not Redistribute
#

# install dependencies

include_recipe 'python'
include_recipe 'python::pip'
include_recipe 'python::virtualenv'

python_pip 'virtualenvwrapper' do
  action :install
end

include_recipe 'mongodb::10gen_repo'
include_recipe 'mongodb'

# install python stuff

venv_directory = '/home/vagrant'

python_virtualenv "#{venv_directory}/.virtualenvs/notify" do
    interpreter 'python2.7'
    action :create
end

python_pip 'install-requirements' do
  options '-r'
  package_name "/home/vagrant/notify/requirements.txt"
  virtualenv "/home/vagrant/.virtualenvs/notify"
  action :install
end