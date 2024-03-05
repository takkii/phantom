# frozen_string_literal: true

require 'open3'
require 'fileutils'

# Installer runner.
class InstallerRunner
  # default encoding utf-8, change encode here.
  def self.encoding_style
    Encoding.default_internal = 'UTF-8'
    Encoding.default_external = 'UTF-8'
  end

  def self.run
    encoding_style
    if File.exist?(File.expand_path('~/dict/php_dict.txt'))
      puts 'Already have a php_dict File ... do nothing.'
    else
      stdout_php = Open3.capture3("php ./dict/php_dict.php")
      stdout_php
      FileUtils.mv(['./php_dict.txt'], "./dict")
      puts 'Created, ./dict/php_dict.txt'
    end
  end
end

begin
  InstallerRunner.run
rescue StandardError => e
  puts e.backtrace
ensure
  GC.compact
end

__END__
