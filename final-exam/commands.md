# commands.md — exact commands I ran, per part

## Part A — Threads, Mapping & Signals

```bash
cd ~/os-se-p20240002/final-exam/partA_threads

# Write and compile thread_demo.c
gcc -o thread_demo thread_demo.c -lpthread
./thread_demo

# Capture 1:1 user→kernel (LWP) mapping while process is alive
./thread_demo &
sleep 1 && ps -eLf | grep thread_demo | grep -v grep > thread_map.txt
cat thread_map.txt

# Write and compile signal_demo.c
gcc -o signal_demo signal_demo.c
./signal_demo
# Press Ctrl+C to send SIGINT and trigger handler
```

## Part B — Permissions, Special Bits

```bash
cd ~/os-se-p20240002/final-exam/partB_security

# Create directory tree
mkdir -p ~/techcorp/shared ~/techcorp/private
echo "secret data" > ~/techcorp/private/secret.txt

# Set permissions using octal and symbolic
chmod 600 ~/techcorp/private/secret.txt
chmod 711 ~/techcorp/shared

# Save permission report
ls -l ~/techcorp/private/secret.txt > perm_report.txt
ls -ld ~/techcorp/shared >> perm_report.txt
stat ~/techcorp/private/secret.txt >> perm_report.txt
stat ~/techcorp/shared >> perm_report.txt

# Set setgid and sticky bit
chmod g+s ~/techcorp/shared
chmod +t ~/techcorp/shared
ls -ld ~/techcorp/shared

# Build and set setuid binary
gcc -o setuid_demo setuid_demo.c
chmod u+s setuid_demo
./setuid_demo

# Append to report
echo "--- Special Bits ---" >> perm_report.txt
ls -ld ~/techcorp/shared >> perm_report.txt
./setuid_demo >> perm_report.txt
```

## Part C — Bash Scripting, PATH & Safe Scanning

```bash
# Create greeter script
mkdir -p ~/bin
chmod +x ~/bin/greeter

# Add ~/bin to PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Run greeter by name only
greeter

# Save path report
echo "PATH=$PATH" > ~/os-se-p20240002/final-exam/partC_scripting/path_report.txt
which greeter >> ~/os-se-p20240002/final-exam/partC_scripting/path_report.txt
type greeter >> ~/os-se-p20240002/final-exam/partC_scripting/path_report.txt

# Create test files
mkdir -p ~/testfiles/readable ~/testfiles/mixed
echo "file one content" > ~/testfiles/readable/file1.txt
echo "file two content" > ~/testfiles/readable/file2.txt
echo "file three" > ~/testfiles/mixed/file3.txt
chmod 000 ~/testfiles/mixed/file3.txt

# Run collector
chmod +x ~/bin/collector
collector

# Copy scripts to exam folder
cp ~/bin/greeter ~/os-se-p20240002/final-exam/partC_scripting/scripts/
cp ~/bin/collector ~/os-se-p20240002/final-exam/partC_scripting/scripts/
```

## Part D — Race Condition & flock

```bash
# Initialize stock file
echo 100 > ~/stock.txt

# Create and test buy_reactor_core
chmod +x ~/bin/buy_reactor_core
buy_reactor_core alice 5
cat ~/stock.txt

# Create swarm
chmod +x ~/bin/swarm

# Run swarm 3 times (patched with flock) and record results
OBS=~/os-se-p20240002/final-exam/partD_secure/observations.txt
echo "=== Patched Runs (with flock) ===" > "$OBS"

echo 100 > ~/stock.txt
echo -n "Run 1: " >> "$OBS"
swarm | tail -1 >> "$OBS"

echo 100 > ~/stock.txt
echo -n "Run 2: " >> "$OBS"
swarm | tail -1 >> "$OBS"

echo 100 > ~/stock.txt
echo -n "Run 3: " >> "$OBS"
swarm | tail -1 >> "$OBS"

cat "$OBS"

# Copy scripts to exam folder
cp ~/bin/buy_reactor_core ~/os-se-p20240002/final-exam/partD_secure/scripts/
cp ~/bin/swarm ~/os-se-p20240002/final-exam/partD_secure/scripts/
```

## Part E — Backups & cron

```bash
# Create sample project
mkdir -p ~/sample_project/src ~/sample_project/config
echo "main code" > ~/sample_project/src/main.py
echo "settings" > ~/sample_project/config/settings.conf

# Run backup_project 6 times to trigger pruning (keep newest 4)
chmod +x ~/bin/backup_project
for i in {1..6}; do backup_project; sleep 1; done
ls -lh ~/project_backups/

# Create timed_job and backup_exam
chmod +x ~/bin/timed_job
chmod +x ~/bin/backup_exam
mkdir -p ~/exam-backups

# Set up per-user crontab (crontab -e) with 4 entries:
# * * * * * $HOME/bin/timed_job $HOME/os-se-p20240002/final-exam/partE_automation/logs/cron_recurring.log
# 35 14 * * * $HOME/bin/timed_job $HOME/os-se-p20240002/final-exam/partE_automation/logs/cron_oneshot.log
# */5 * * * * $HOME/bin/backup_exam
# 0 16 * * * $HOME/bin/backup_exam
crontab -e

# Wait for cron to fire then save report
REPORT=~/os-se-p20240002/final-exam/partE_automation/cron_report.txt
echo "=== crontab -l ===" > "$REPORT"
crontab -l >> "$REPORT"
echo "=== cron_recurring.log ===" >> "$REPORT"
cat ~/os-se-p20240002/final-exam/partE_automation/logs/cron_recurring.log >> "$REPORT"
echo "=== cron_oneshot.log ===" >> "$REPORT"
cat ~/os-se-p20240002/final-exam/partE_automation/logs/cron_oneshot.log >> "$REPORT"
echo "=== exam-backups listing ===" >> "$REPORT"
ls -lh ~/exam-backups/ >> "$REPORT"

# Copy scripts to exam folder
cp ~/bin/backup_project ~/os-se-p20240002/final-exam/partE_automation/scripts/
cp ~/bin/timed_job ~/os-se-p20240002/final-exam/partE_automation/scripts/
cp ~/bin/backup_exam ~/os-se-p20240002/final-exam/partE_automation/scripts/
```
