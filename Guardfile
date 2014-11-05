guard 'remote-sync',
  :source => ".",
  :destination => '/home/vagrant/projects/mobile_data_ana',
  :user => 'vagrant',
  :remote_port => 2200,
  :remote_address => 'r',
  :cli => "--color",
  :delete => false,
  :sync_on_start => true do
  watch(%r{^.+\.(js|xml|php|class|config|py)$})
end


