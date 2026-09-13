#!/usr/bin/env ruby
workflow_dir = File.expand_path(__dir__)
domains_file = File.join(workflow_dir, "domains.txt")
shortcut = ARGV.join(" ").strip

if shortcut.empty? || shortcut.match?(/\s/)
  puts "Usage: wp-del shortcut"
  exit 0
end

lines = File.readlines(domains_file, chomp: true)
remaining = lines.reject { |line| line.split(/\s+/, 2).first == shortcut }

if remaining.length == lines.length
  puts "Domain shortcut not found: #{shortcut}"
  exit 0
end

File.write(domains_file, remaining.empty? ? "" : "#{remaining.join("\n")}\n")
puts "Deleted domain: #{shortcut}"
