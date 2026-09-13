# WordPress Site Shortcuts for Alfred

Open a saved WordPress site and page in Firefox. Domains containing `test` (case-insensitive, including `.test` and `test.example.com`) open in Firefox Developer Edition instead. This checks the hostname only; `test` in a page path, query string, or shortcut name does not change the browser.

## Open a page

1. Open Alfred and type `wp` (or `wp sb` to filter the sites).
2. Select a site and press Enter.
3. Type a page shortcut, such as `admin`, `plugins`, or `users`.
4. Select the page and press Enter to open it in Firefox.

For example, selecting `sb` and then `admin` opens:

```text
https://saferbaby.org.au/wp-admin
```

## Add a domain

Type this in Alfred and press Enter:

```text
wp-add example https://example.com
```

Replace `example` with your shortcut and the URL with your site's address.

- Include `https://` (or `http://` for sites that require it).
- Use a shortcut starting with a letter or number, followed by letters, numbers, hyphens, or underscores. No spaces.
- Lowercase shortcuts are easiest to remember. Add/delete commands match shortcut capitalization exactly.
- An existing shortcut will not be overwritten. To change its address, edit `domains.txt`, or delete the shortcut and add it again.

Run `wp example` to check the new entry. The management commands currently do not display a confirmation notification.

## Remove a domain

Type this in Alfred and press Enter:

```text
wp-del example
```

This removes the saved shortcut only; it does not delete or change the website.

## Edit domains directly

Open `domains.txt` in this workflow folder with a plain-text editor. Each line contains a shortcut, a space, and the site's base URL:

```text
sb https://saferbaby.org.au
example https://example.com
local http://localhost
```

Add a line to add a domain, change a line to update it, or delete the whole line to remove it. Keep shortcuts unique and save the file.

## Add a page

Open `pages.txt` in this workflow folder with a plain-text editor. Add a line containing a shortcut, a space, and the page path:

```text
posts /wp-admin/edit.php
media /wp-admin/upload.php
home /
```

Page shortcuts are shared by every domain. The workflow joins the selected domain with the page path. For example, `example` followed by `posts` opens `https://example.com/wp-admin/edit.php`.

Use a path beginning with `/`, not a full website URL. Query parameters are supported; write them directly without quotes or escaping:

```text
forms /wp-admin/admin.php?page=gf_edit_forms
fw /wp-admin/admin.php?page=wdf-ip-lockout&view=global-ip
```

Keep page shortcuts unique and without spaces. Save the file, then run `wp` again to see the changes. There is currently no Alfred command for adding pages.

## Remove or change a page

In `pages.txt`:

- **Remove:** delete the entire line for the shortcut.
- **Rename:** change the shortcut at the start of the line.
- **Change destination:** edit the path after the shortcut.

Save the file. This changes the shortcut list for all domains; it does not modify any WordPress site. There is currently no Alfred command for deleting pages.

Both data files support blank lines and comments starting with `#`. To temporarily hide a shortcut, put `#` at the start of its line.

## Included shortcut library

`pages.txt` contains 153 shortcuts, sorted alphabetically by shortcut. Existing short aliases such as `def`, `humm`, `ass`, `crawl`, `forms`, and `wpv-backups` are preserved. `forms` still opens Gravity Forms; use `forminator-forms` for Forminator.

After choosing a site, type a plugin name to narrow the page list, or type a specific shortcut such as `hummingbird-caching`.

| Area | Example shortcuts |
| --- | --- |
| WordPress content | `posts`, `post-add`, `posts-drafts`, `pages`, `page-add`, `categories`, `tags`, `comments` |
| Media and appearance | `media`, `media-add`, `menus`, `widgets`, `customize`, `site-editor`, `theme-add` |
| Maintenance and settings | `updates`, `health`, `health-info`, `permalinks`, `reading`, `discussion`, `plugins-inactive`, `plugins-updates` |
| Users and privacy | `profile`, `user-add`, `privacy`, `privacy-export`, `privacy-erase` |
| Multisite | `network`, `network-sites`, `network-plugins`, `network-settings`, `network-users` |
| Branda | `branda-login-screen`, `branda-admin-menu`, `branda-maintenance`, `branda-smtp`, `branda-email-logs`, `branda-tracking-codes` |
| Defender | `defender-scan`, `defender-firewall`, `defender-audit`, `defender-hardening`, `defender-login`, `defender-settings` |
| Forminator | `forminator-forms`, `forminator-polls`, `forminator-quizzes`, `forminator-entries`, `forminator-integrations`, `forminator-reports` |
| Hummingbird | `hummingbird-caching`, `hummingbird-assets`, `hummingbird-performance`, `hummingbird-advanced`, `hummingbird-uptime` |
| Hustle | `hustle-popups`, `hustle-slideins`, `hustle-embeds`, `hustle-social`, `hustle-entries` |
| SmartCrawl | `smartcrawl-titles`, `smartcrawl-schema`, `smartcrawl-sitemap`, `smartcrawl-redirects`, `smartcrawl-indexing` |
| Smush | `smush`, `smush-cdn`, `smush-directory`, `smush-lazy-preload`, `smush-settings` |

### Availability and versions

The workflow shows a shared list; it does not detect installed plugins. Plugin links require the relevant plugin and appropriate user permissions. Some screens require Pro or an enabled module. Multisite shortcuts require a multisite installation and network permissions; network-managed plugin screens may require changing `/wp-admin/admin.php` to `/wp-admin/network/admin.php`. Appearance screens depend on the active theme.

These shortcuts open management screens. For example, `updates` opens the update screen and `privacy-erase` opens the erasure request screen; selecting the shortcut does not submit those actions.

New plugin destinations were checked against menu definitions in the official WordPress.org plugin downloads on 5 September 2026: Branda 3.4.31, Defender 6.2.2, Forminator 1.57.2, Hummingbird 3.21.2, Hustle 7.8.14.2, SmartCrawl 3.16.4, and Smush 4.3.2. They have not been tested inside every saved website. Older plugin versions may use different destinations, particularly Defender and Smush. If a shortcut opens the dashboard or an unavailable-page message, navigate to the desired screen and copy its path into `pages.txt`.

Reference sources: [WordPress administration screens](https://wordpress.org/documentation/article/administration-screens/), [WPMU DEV plugin documentation](https://wpmudev.com/docs/wpmu-dev-plugins/), and official plugin source: [Branda](https://plugins.svn.wordpress.org/branda-white-labeling/trunk/), [Defender](https://plugins.svn.wordpress.org/defender-security/trunk/), [Forminator](https://plugins.svn.wordpress.org/forminator/trunk/), [Hummingbird](https://plugins.svn.wordpress.org/hummingbird-performance/trunk/), [Hustle](https://plugins.svn.wordpress.org/wordpress-popup/trunk/), [SmartCrawl](https://plugins.svn.wordpress.org/smartcrawl-seo/trunk/), [Smush](https://plugins.svn.wordpress.org/wp-smushit/trunk/).

## Find the correct workflow folder

In Alfred Preferences → Workflows, select **WP Site Shortcuts**, then use **Open in Finder** from the workflow's context menu.

The active folder was confirmed on 5 September 2026 as:

```text
~/Library/CloudStorage/OneDrive-Personal/Application Settings/Alfred/Alfred.alfredpreferences/workflows/user.workflow.7210C896-4D98-48B6-A5B1-81AC1A84FB87
```

Edit the files in that folder. The nearby `-Vicar Amelia`, `-Vicar Amelia-2`, and `-Micolash` profile copies are separate copies; changes to their data files will not update the active workflow.

## Troubleshooting

If an entry does not appear, save the data file, leave Alfred's current results, and run `wp` again. Check that the line has both a shortcut and a URL/path, and that you edited the active workflow folder.

Runtime diagnostics are written to:

```text
~/Library/Logs/WP Site Shortcuts/workflow.jsonl
```

The log records site/page filtering and the URL received by the Firefox opener. `WORKFLOW_HANDOFF.md` contains technical repair notes. The complete site → page → Firefox flow was confirmed working by the user on 5 September 2026.

## Page icons

Page results include local PNG icons: original colorful symbols for WordPress screens and official artwork for Branda, Defender, Forminator, Hummingbird, Hustle, SmartCrawl, Smush, UpdraftPlus, and WPvivid. Plugin artwork is sourced from the publishers’ WordPress.org listings; exact source URLs are recorded in `icons/sources/plugins.json`. Animated artwork is saved as a static frame. Plugin names and artwork belong to their respective owners.

Icons are selected automatically in `wp_icons.rb` by the destination’s plugin page parameter, then by shortcut name for WordPress screens. Existing aliases therefore get the same plugin artwork as their longer equivalents. Unknown shortcuts use the dashboard symbol, with the workflow icon as a fallback if an asset is missing. You do not need to change the two-column format in `pages.txt`.

All images are stored in `icons/`; no network requests or extra dependencies are needed when using Alfred. The original core symbols can be rebuilt with `icons/sources/generate_core.py` (Pillow required only for rebuilding).
