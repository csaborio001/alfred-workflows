#!/usr/bin/env ruby
require "json"
require_relative "wp_log"
require_relative "wp_icons"

workflow_dir = File.expand_path(__dir__)
domains_file = File.join(workflow_dir, "domains.txt")
pages_file = File.join(workflow_dir, "pages.txt")
domain = ENV["wp_domain"].to_s
arguments = ARGV.join(" ").downcase.split

def entries(path)
  File.readlines(path, chomp: true).each_with_object([]) do |line, result|
    shortcut, value = line.strip.split(/\s+/, 2)
    next if shortcut.nil? || value.nil? || shortcut.start_with?("#")
    result << [shortcut, value]
  end
end

domains = entries(domains_file)
selected_index = domain.empty? ? arguments.index { |argument| domains.any? { |shortcut, value| [shortcut.downcase, value.downcase].include?(argument) } } : arguments.index { |argument| domains.any? { |shortcut, value| value == domain && [shortcut.downcase, value.downcase].include?(argument) } }
selected_shortcut = selected_index && arguments[selected_index]
selected_domain = domains.find { |shortcut, value| [shortcut.downcase, value.downcase].include?(selected_shortcut) }
domain = selected_domain[1] if domain.empty? && selected_domain
query_terms = selected_index ? arguments.each_with_index.reject { |_argument, index| index == selected_index }.map(&:first) : arguments

def url_for(domain, path)
  "#{domain.sub(%r{/$}, "")}/#{path.sub(%r{^/}, "")}"
end

if domain.empty?
  wp_log("pages_missing_domain", {arguments: ARGV})
  puts JSON.generate("items" => [{"title" => "Select a WordPress site first", "subtitle" => "Press Escape and run wp again", "valid" => false}])
  exit
end

items = entries(pages_file).each_with_object([]) do |(shortcut, path), result|
  url = url_for(domain, path)
  haystack = "#{shortcut} #{path} #{url}".downcase
  next unless query_terms.empty? || query_terms.all? { |term| haystack.include?(term) }
  result << { "uid" => "#{domain}:#{shortcut}", "type" => "default", "title" => shortcut, "subtitle" => url, "arg" => url, "icon" => { "path" => page_icon(shortcut, path) }, "valid" => true }
end

items = [{ "title" => "No matching pages", "subtitle" => "Try another page name", "valid" => false }] if items.empty?
wp_log("pages", {arguments: ARGV, domain: domain, count: items.length})
puts JSON.generate("items" => items)
