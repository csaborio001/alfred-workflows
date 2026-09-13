#!/usr/bin/env ruby
require "json"
require_relative "wp_log"

workflow_dir = File.expand_path(__dir__)
domains_file = File.join(workflow_dir, "domains.txt")
query_terms = ARGV.join(" ").downcase.split

def entries(path)
  File.readlines(path, chomp: true).each_with_object([]) do |line, result|
    shortcut, value = line.strip.split(/\s+/, 2)
    next if shortcut.nil? || value.nil? || shortcut.start_with?("#")
    result << [shortcut, value]
  end
end

domains = entries(domains_file)
items = domains.each_with_object([]) do |(shortcut, domain), result|
  haystack = "#{shortcut} #{domain}".downcase
  next unless query_terms.empty? || query_terms.all? { |term| haystack.include?(term) }

  result << {
    "uid" => shortcut,
    "type" => "default",
    "title" => shortcut,
    "subtitle" => domain,
    # The selected domain travels in variables; start the page query empty.
    "arg" => "",
    "variables" => { "wp_domain" => domain },
    "valid" => true
  }
end

items = [{
  "title" => "No matching WordPress sites",
  "subtitle" => "Add a domain with: wp-add shortcut https://example.com",
  "valid" => false
}] if items.empty?

wp_log("sites", {arguments: ARGV, count: items.length})
puts JSON.generate("items" => items)
