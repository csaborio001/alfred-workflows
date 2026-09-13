require 'json'
require 'fileutils'
def wp_log(stage, details = {})
  directory = File.expand_path('~/Library/Logs/WP Site Shortcuts')
  FileUtils.mkdir_p(directory)
  File.open(File.join(directory, 'workflow.jsonl'), 'a', 0600) do |file|
    file.puts JSON.generate({time: Time.now.to_s, stage: stage, workflow: __dir__, alfred_preferences: ENV['alfred_preferences']}.merge(details))
  end
rescue SystemCallError => error
  warn "Workflow logging failed: #{error.message}"
end
