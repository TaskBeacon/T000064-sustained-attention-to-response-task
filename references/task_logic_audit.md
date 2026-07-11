# SART Task Logic Audit

## 1. Paradigm Intent
Fixed high-go SART measuring sustained-attention lapses and response inhibition.

## 2. Block/Trial Workflow
18 practice trials then one continuous 225-trial scored block. Trial: digit 250 ms then mask 900 ms.

## 3. Condition Semantics
`go` is every digit except 3; `no_go` is digit 3.

## 4. Response and Scoring Rules
Space during digit or mask is a go hit or no-go false alarm. No response is a go omission or no-go correct rejection. RT is from digit onset.

## 5. Stimulus Layout Plan
Central digit and mask; five digit heights 12-29 mm; mask diameter 29 mm.

## 6. Trigger Plan
Digit go/no-go 20/21, mask 30, go response 40, commission 41, omission 42.

## 7. Architecture Decisions (Auditability)
PsyFlow owns IDs, timing, triggers, capture, and data. Task-local planning is required for exact digit counts and size mapping.

## 8. Inference Log
Font sizes are exactly balanced within digit rather than merely assigned at random. Practice feedback is block-level only.
