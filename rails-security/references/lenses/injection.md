# Injection Lens

Untrusted input reaching Rails sinks: SQL, HTML, shell, files, URLs, headers, templates, and serialized data.

## Map

```bash
grep -rn "raw(\|\.html_safe\|<%==\|!= \|sanitize(\|simple_format\|render inline\|_html:" app/
grep -rn "Arel.sql\|find_by_sql\|where(\"\|order(params\|reorder(params\|pluck(params\|group(params\|having(params\|delete_all\|update_all" app/
grep -rn "eval(\|system(\|exec(\|spawn(\|IO\.popen\|Open3\|%x\[\|\`" app/ lib/
grep -rn "Kernel.open\|URI.open\|OpenURI\|Net::HTTP\|Faraday\|HTTParty\|RestClient" app/ lib/
grep -rn "send_file\|send_data\|File\.open\|File\.read\|File\.write\|response\.headers" app/
grep -rn "Marshal\.load\|YAML\.load\|constantize\|redirect_to params\|allow_other_host" app/ lib/
```

## Search

- SQL: interpolated strings in `where`, `order`, `joins`, `group`, `having`, `select`, `delete_all`, `update_all`; `Arel.sql` and `find_by_sql` fed user input; LIKE queries without `sanitize_sql_like`; sort/filter params choosing column names or directions without an allowlist.
- XSS: `raw`, `.html_safe`, `<%==`, Haml `!=`, `_html` translation keys, weak `sanitize` configs, Markdown/ActionText rendered without an allowlist sanitizer, JSON embedded in `<script>` without `json_escape`, unquoted HTML attributes holding user input, user URLs in `link_to` (`javascript:` scheme), SVG or HTML uploads served from the application origin.
- Command and code execution: `system`/backticks/`%x`/`Open3` with interpolated strings — the safe shape is the argument-array form; `eval` or `constantize` on user input; `Kernel#open` and bare `open` on user strings (a leading `|` runs a command); `render inline:` or user-chosen template names.
- File paths: user-controlled filenames in `File.*`, `send_file`, `send_data`, and export paths; verify expanded paths stay under the intended directory; stored files use generated names.
- SSRF: user URLs reaching `Net::HTTP`, `Faraday`, `HTTParty`, `RestClient`, `URI.open`, webhook senders, URL previews, imports, and attach-from-URL. Defenses must reject non-HTTP schemes, embedded credentials, localhost/private/link-local/metadata IPs in every encoding, and redirects into blocked hosts — with timeouts and size limits.
- Deserialization: `Marshal.load` or `YAML.load` (want `safe_load`) on user, cookie, or job data; legacy cookie serializers; user-controlled `constantize`.
- Redirects and headers: `redirect_to` on params, `return_to`/`next`/`url`-style params, `allow_other_host: true`; user input in `response.headers`, `Content-Disposition` filenames, or cookies must reject CRLF.
- Format validation anchored with `\A`/`\z`, not `^`/`$`.
- Sink fan-out: when one field reaches an unsafe sink, grep every view, partial, serializer, mailer, and JSON builder rendering the same field.

## Evidence bar

The tainted source, its path to the sink, and the payload shape that exploits it — `file:lines` for each hop.

## Exclude

Sinks reachable only by developers or deploy tooling (rake tasks, seeds, migrations), and escaping Rails already guarantees by default.
