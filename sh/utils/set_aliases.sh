# ###############################################################
# Helper function
# ###############################################################

function _exec_cmd()
{
    # Destructure command script & args.
    args=($@)
    args_len=${#args[@]}
    s_path=${args[0]}
    s_args=${args[@]:1:$args_len}

    # Execute script.
    pushd $STESTS_HOME
    pipenv run python $s_path $s_args
    popd -1
}

# ###############################################################
# ALIASES: stack 
# ###############################################################

alias stests-stack-update=$STESTS_PATH_SH/stack/update.sh

# ###############################################################
# ALIASES: workers
# ###############################################################

alias stests-interactive='$STESTS_PATH_SH/workers/interactive.sh unified'
alias stests-interactive-monitoring='$STESTS_PATH_SH/workers/interactive.sh monitoring'
alias stests-interactive-workflows='$STESTS_PATH_SH/workers/interactive.sh workflows'

alias stests-workers-start=$STESTS_PATH_SH/workers/start.sh
alias stests-workers-status=$STESTS_PATH_SH/workers/status.sh
alias stests-workers-stop=$STESTS_PATH_SH/workers/stop.sh
alias stests-workers-reload=$STESTS_PATH_SH/workers/reload.sh
alias stests-workers-reset-logs=$STESTS_PATH_SH/workers/reset_logs.sh

# ###############################################################
# ALIASES: cache - flush
# ###############################################################

alias stests-flush='$STESTS_PATH_SH/cache/flush.sh'
alias stests-flush-infra='$STESTS_PATH_SH/cache/flush_infra.sh'

# ###############################################################
# ALIASES: cache - ls
# ###############################################################

alias stests-ls-contracts='_exec_cmd $STESTS_PATH_CLI/list_contracts.py'

alias stests-ls-networks='_exec_cmd $STESTS_PATH_CLI/list_networks.py'
alias stests-ls-network-faucet-balance='_exec_cmd $STESTS_PATH_CLI/list_network_faucet_balance.py'
alias stests-ls-network-faucet-key='_exec_cmd $STESTS_PATH_CLI/list_network_faucet_key.py'

alias stests-ls-nodes='_exec_cmd $STESTS_PATH_CLI/list_nodes.py'
alias stests-ls-node-bonding-key='_exec_cmd $STESTS_PATH_CLI/list_node_bonding_key.py'

alias stests-ls-run='_exec_cmd $STESTS_PATH_CLI/list_run.py'
alias stests-ls-run-deploys='_exec_cmd $STESTS_PATH_CLI/list_run_deploys.py'
alias stests-ls-runs='_exec_cmd $STESTS_PATH_CLI/list_runs.py'

# ###############################################################
# ALIASES: cache - set
# ###############################################################

alias stests-set-contracts='_exec_cmd $STESTS_PATH_CLI/set_contracts.py'

alias stests-set-network='_exec_cmd $STESTS_PATH_CLI/set_network.py'
alias stests-set-network-faucet-key='_exec_cmd $STESTS_PATH_CLI/set_network_faucet_key.py'
alias stests-set-network-status='_exec_cmd $STESTS_PATH_CLI/set_network_status.py'

alias stests-set-node='_exec_cmd $STESTS_PATH_CLI/set_node.py'
alias stests-set-node-bonding-key='_exec_cmd $STESTS_PATH_CLI/set_node_bonding_key.py'
alias stests-set-node-status='_exec_cmd $STESTS_PATH_CLI/set_node_status.py'

# ###############################################################
# ALIASES: chain - view
# ###############################################################

alias stests-view-balance='_exec_cmd $STESTS_PATH_CLI/view_balance.py'

alias stests-view-block-info='_exec_cmd $STESTS_PATH_CLI/view_block_info.py'
alias stests-view-deploy-info='_exec_cmd $STESTS_PATH_CLI/view_deploy_info.py'

# ###############################################################
# ALIASES: generators
# ###############################################################

function _exec_generator()
{
    # Destructure generator type & args.
    args=($@)
    args_len=${#args[@]}
    g_type=${args[0]}
    g_args=${args[@]:1:$args_len}


    # Execute generator.
    _exec_cmd $STESTS_PATH_GENERATORS/wg_$g_type $g_args
}

# WG-100: Token transfer - client contract.
alias stests-wg-100='_exec_generator 100'

# WG-110: Token transfer - stored contract.
alias stests-wg-110='_exec_generator 110'

# WG-200: Counter - client contract.
alias stests-wg-200='_exec_generator 200'

# WG-210: Counter - stored contract.
alias stests-wg-210='_exec_generator 210'
