# Handbook

## When to use
The owner asks what you do, how you are set up, or how to keep, copy, or rebuild you.

Your copy-critic skills live in your skills library, not on this computer: load them with the Skill tool (or Read the path your skill catalog gives). Retyping them is the slow part, so do nothing else extra: no draft, no re-reading, no second pass.

## Steps (four steps)
1. **One batch of parallel calls:** list your routines; call GetMcpServerStatus; load each copy-critic skill except this one with the Skill tool (this one is already loaded); and run one shell command: `grep -i origin /workspace/copy-critic/setup.md | head -1`, plus `test -f` on any skill path your catalog lists (echo the ones that exist).
2. **One file write** of `/workspace/copy-critic/handbook.md` with your file-write tool, in this order:
   - "# Landing Page Copy Critic handbook" and the date in the owner's time zone with a zone label.
   - Profile; Job and guardrails; Memory (each fact verbatim, without its learned date); Routines (name, trigger, on or off exactly as listed; paused means off).
   - "## How to recreate": numbered steps a stranger could follow in a blank bot.
   - "## Connectors": one line per connector GetMcpServerStatus shows connected (GitHub only if a GitHub read succeeded in this chat; "- None connected." if none), then exactly "- Origin: no connector; access is checked by reading the repo." and, if the grep found one, "- Origin repo in setup.md: " plus that line.
   - "## Skills": for each of the 6 copy-critic skills, "### name", then its full text exactly as loaded inside a `~~~~` fence. If `test -f` found its file, write only the line `@@FILE <path>@@` instead. If a load failed, write the skill name and the error it returned.
3. **This fixed shell command**, unchanged:

```sh
cd /workspace/copy-critic && awk '/^@@FILE /{f=$2; sub(/@@$/,"",f); print "~~~~"; while ((getline l < f) > 0) print l; close(f); print "~~~~"; next} 1' handbook.md > h.tmp && { cat h.tmp; printf '\n## Workspace files\n\n### setup.md\n~~~~\n'; cat setup.md; printf '~~~~\n\n### Last reviews\n~~~~\n'; tail -n 30 reviews.md; printf '~~~~\n'; } > handbook.md && rm h.tmp
```

4. Send `/workspace/copy-critic/handbook.md` with SendToUser as an attachment (`file://` path), plus 3 lines: what changed since the last handbook, how many skills and routines, and anything that looks broken.

Leave out webhook keys, tokens, passwords, and account emails.

## Never
Never write "could not read" for a skill without trying to load it, and never shorten or summarize a skill body.
