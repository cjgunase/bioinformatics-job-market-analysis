# Atomic extraction prompt v01

Pass A only: identify short verbatim sentences or bullets that explicitly state
a skill, tool, responsibility, qualification, education condition, or experience
condition. Preserve exact wording and offsets. Split compound statements only
when each proposed item is textually supported. Do not assign taxonomy labels,
infer unstated tools, or treat titles/marketing/benefits as requirements. Record
provider/model/version, parameters, input/output hashes, timestamp, and retries
for every production model call. This prompt is a versioned draft and requires
fixture validation before any production model is configured.
