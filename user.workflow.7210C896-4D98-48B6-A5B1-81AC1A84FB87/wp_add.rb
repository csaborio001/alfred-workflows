#!/usr/bin/env ruby
require "uri"

workflow_dir = File.expand_path(__dir__)
domains_file = File.join(workflow_dir, "domains.txt")
shortcut, domain = ARGV.join(" ").strip.split(/\s+/, 2)

if shortcut.nil? || domain.nil? || shortcut !~ /\A[a-zA-Z0-9][a-zA-Z0-9_-]*\z/
  puts "Usage: wp-add shortcut https://example.com"
  exit 0
end

begin
  uri = URI.parse(domain)
  valid_url = ["http", "https"].include?(uri.scheme) && !uri.host.nil?
rescue URI::InvalidURIError
  valid_url = false
end

unless valid_url
  puts "Domain must be an http or https URL"
  exit 0
end

domains = File.readlines(domains_file, chomp: true)
if domains.any? { |line| line.split(/\s+/, 2).first == shortcut }
  puts "Domain shortcut already exists: #{shortcut}"
  exit 0
end

File.open(domains_file, "a") { |file| file.puts "#{shortcut} #{domain.sub(%r{/$}, "")}" }
puts "Added #{shortcut} -> #{domain}"
