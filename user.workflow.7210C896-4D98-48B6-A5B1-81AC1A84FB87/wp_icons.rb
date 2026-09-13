# Local icons selected by destination, so aliases and new shortcuts inherit them.
require 'uri'
def page_icon(shortcut, path)
  page = URI.decode_www_form(path.split('?', 2).last.to_s).to_h.fetch('page', '')
  plugin = case page
           when /\A(?:wp-defender|wdf-)/ then 'defender'
           when /\Awphb/ then 'hummingbird'
           when /\Abranding/ then 'branda'
           when /\Awds[_-]/ then 'smartcrawl'
           when /\Aforminator/ then 'forminator'
           when /\Ahustle/ then 'hustle'
           when /\Asmush/ then 'smush'
           when /\Aupdraftplus/ then 'updraftplus'
           when /\Awpvivid/ then 'wpvivid'
           when /\Asnapshot/ then 'backup'
           when /\Agf_/ then 'forms'
           when /\Abreakdance/ then 'themes'
           end
  category = case shortcut
             when /\A(user|profile)/ then 'users'
             when /\A(post|writing)/ then 'posts'
             when /\A(page|reading)/ then 'pages'
             when /\Amedia/ then 'media'
             when /\A(theme|customize|site-editor|widgets|menus)/ then 'themes'
             when /\Aplugin/ then 'plugins'
             when /\Anetwork/ then 'network'
             when /\A(comment|discussion)/ then 'comments'
             when /\Ahome\z/ then 'home'
             when /\Aprivacy/ then 'privacy'
             when /\A(login|reg)\z/ then 'login'
             when /\Aupdates/ then 'updates'
             when /\Ahealth/ then 'health'
             when /\Aimport/ then 'import'
             when /\Aexport/ then 'export'
             when /\A(categories|tags)/ then 'tags'
             when /\Apermalinks/ then 'link'
             when /\Atools/ then 'tools'
             when /\A(settings|gen|st)\z/ then 'settings'
             else 'dashboard'
             end
  relative = "icons/#{plugin || category}.png"
  File.file?(File.join(__dir__, relative)) ? relative : 'icon.png'
end
