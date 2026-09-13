#!/usr/bin/env ruby
require 'uri'
require_relative 'wp_log'
url = ARGV.fetch(0, '')
wp_log('open_received', {arguments: ARGV})
begin
  uri = URI.parse(url)
  raise URI::InvalidURIError unless ['https', 'http'].include?(uri.scheme) && uri.host
rescue URI::InvalidURIError
  warn 'No valid website URL received. Run wp and select a site again.'
  wp_log('open_rejected')
  exit 1
end
# Match the hostname only, not the page path or query string.
browser = uri.host.downcase.include?('test') ? 'org.mozilla.firefoxdeveloperedition' : 'org.mozilla.firefox'
success = system('/usr/bin/open', '-b', browser, '--', url)
wp_log('open_finished', {success: success, exit_status: $?.exitstatus, browser: browser})
exit(success ? 0 : 1)
