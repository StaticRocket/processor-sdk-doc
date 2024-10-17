#!/bin/bash
### Wrapper to calculate deltas between two commits


HELP_STRING="
Check if git branch or commit <NEW> generates any new build output running
<COMMAND> based on git branch or commit <OLD>.

check-warn.sh [OPTIONS]

DIFF OPTIONS:
  -a OLD             git branch or commit ID OLD as the base, 'HEAD' is
                     acceptable
  -b NEW             git branch or commit ID NEW for checking WARNING(s), 'HEAD'
                     is acceptable
  -m, --merge        automatically pick the merge-base for the given commits
  --                 everything after this is the COMMAND to be executed

OTHER OPTIONS:
  -h, --help         this message
"

trap restore_branch 1 2 3 6 15

usage()
{
	echo "${HELP_STRING}"
	exit "$1"
}

save_branch()
{
	# get current branch name or commit ID
	_cbr=$(git branch | sed -n '/\* /s///p')
	if [[ "$_cbr" == "(HEAD detached"* ]]; then
		_cbr=$(git rev-parse HEAD)
	fi
}

restore_branch()
{
	[ -z "$_cbr" ] || git checkout "$_cbr"
}

summary()
{
	local _num

	rm -f _new-warn.log
	diff --changed-group-format="%>" --unchanged-group-format="" \
		_a.log _b.log > _new-warn.log

	_num=$(wc -l < _new-warn.log)

	echo
	echo "Found $_num new build WARNING(s)."
	echo

	if [ "$_num" != "0" ]; then
		cat _new-warn.log
	fi
}

generate_log()
{
	local git_hash log_name log_path

	git_hash=$1
	log_name=$2

	log_path="${log_name}.log"

	git checkout "${git_hash}" || exit 10

	mkdir -p build

	rm -f "${log_path}"
	"${_cmd[@]}" 2>&1 | tee -a "${log_path}"
}

rev-parse()
{
	local rev
	if ! rev=$(git rev-parse "$1"); then
		printf '%s\n' 'Unable to parse given revisions:'
		printf '  %s\n' "$1"
		exit 2
	fi
	echo "$rev"
}

main()
{
	# do nothing if current workspace is not clean
	if [ -n "$(git status --porcelain --untracked-files=no)" ]
	then
		echo "Error: Current workspace has uncommitted changes"
		exit 4
	fi

	save_branch

	_old=$(rev-parse "${_old}")
	_new=$(rev-parse "${_new}")

	if [ -n "${_merge}" ] && ! _old=$(git merge-base "${_old}" "${_new}")
	then
		echo "Error: Unable to find merge-base for the given commits"
		exit 5
	fi

	generate_log "${_old}" "_a"
	generate_log "${_new}" "_b"

	restore_branch
	summary
}

while [ "$#" -gt 0 ]; do
	case $1 in
	-h | --help) usage 0;;
	-d | --device) shift; _dev=$1; shift;;
	-o | --os) shift; _os=$1; shift;;
	-a) shift; _old=$1; shift;;
	-b) shift; _new=$1; shift;;
	-m | --merge) shift; _merge=1;;
	--) shift; break;;
	*) shift;;
	esac
done
_cmd=("$@")

if [ -z "${_new}" ] || [ -z "${_old}" ] || [ -z "${_cmd[*]}" ]; then
	usage 2
fi

main
