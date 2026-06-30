# Live Modifications

## Curveball A — 3 extra workers
**Issued instruction:** Add 3 extra workers that start only after originals joined; show new LWPs appear then disappear.
**Live value:** 3 extra workers
**Commands run:** Edited thread_demo.c to add EXTRA_THREADS=3 block after join loop. Recompiled and ran. Captured ps -eLf showing new LWPs.
**Screenshot:** partA_threads/images/live_a.png

## Curveball D — Purchase cap = 7
**Issued instruction:** Add per-buyer purchase cap; reject orders above it; re-run swarm.
**Live value:** cap = 7
**Commands run:** Added CAP=7 check to buy_reactor_core before flock block. Re-ran swarm with echo 100 > ~/stock.txt then swarm.
**Screenshot:** partD_secure/images/live_d.png

## Curveball E — Idempotent timed_job with RUNGUARD
**Issued instruction:** Make timed_job idempotent using marker token RUNGUARD; trigger twice and prove 2nd was skipped.
**Live value:** token = RUNGUARD
**Commands run:** Rewrote timed_job to check for RUNGUARD_<date> in logfile before running. Ran timed_job twice, second was skipped.
**Screenshot:** partE_automation/images/live_e.png
