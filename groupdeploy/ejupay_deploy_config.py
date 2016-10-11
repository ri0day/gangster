config46={
'source_host' : '10.0.57.46',
'fetch_dir': '/tmp/from_46_to_prod',

'account-inrpc':
    {
       'group1':['10.20.1.1'],
       'group2':['10.20.1.2'],
       'groupfull':['10.20.1.1','10.20.1.2'],
       'port':8126,
       'instance_dir':'/data/tomcat/ejupay-account-inrpc',
       'war_filename':'account-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-account-inrpc/webapps/account-inrpc.war'
    },

'bill-inrpc':
    {
       'group1':['10.20.1.3'],
       'group2':['10.20.1.4'],
       'groupfull':['10.20.1.3','10.20.1.4'],
       'port':8127,
       'instance_dir':'/data/tomcat/ejupay-bill-inrpc',
       'war_filename':'bill-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-bill-inrpc/webapps/bill-inrpc.war'
    },

'cash-inrpc':
    {
       'group1':['10.20.1.5'],
       'group2':['10.20.1.6'],
       'groupfull':['10.20.1.5','10.20.1.6'],
       'port':8125,
       'instance_dir':'/data/tomcat/ejupay-cash-inrpc',
       'war_filename':'cash-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-cash-inrpc/webapps/cash-inrpc.war'
    },


'channel-inrpc':
    {
       'group1':['10.20.1.1'],
       'group2':['10.20.1.2'],
       'groupfull':['10.20.1.1','10.20.1.2'],
       'port':8124,
       'instance_dir':'/data/tomcat/ejupay-channel-inrpc',
       'war_filename':'channel-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-channel-inrpc/webapps/channel-inrpc.war'
    },

'gateway-inrpc':
    {
       'group1':['10.20.1.3'],
       'group2':['10.20.1.4'],
       'groupfull':['10.20.1.3','10.20.1.4'],
       'port':8129,
       'instance_dir':'/data/tomcat/ejupay-gateway-inrpc',
       'war_filename':'gateway-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-gateway-inrpc/webapps/gateway-inrpc.war'
    },

'gateway-outrpc':
    {
       'group1':['10.20.1.5'],
       'group2':['10.20.1.6'],
       'groupfull':['10.20.1.5','10.20.1.6'],
       'port':8130,
       'instance_dir':'/data/tomcat/ejupay-gateway-outrpc',
       'war_filename':'gateway-outrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-gateway-outrpc/webapps/gateway-outrpc.war'
    },


'kabin-inrpc':
    {
       'group1':['10.20.1.1'],
       'group2':['10.20.1.2'],
       'groupfull':['10.20.1.1','10.20.1.2'],
       'port':8128,
       'instance_dir':'/data/tomcat/ejupay-kabin-inrpc',
       'war_filename':'kabin-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-kabin-inrpc/webapps/kabin-inrpc.war'
    },

'mb-inrpc':
    {
       'group1':['10.20.1.3'],
       'group2':['10.20.1.4'],
       'groupfull':['10.20.1.3','10.20.1.4'],
       'port':8131,
       'instance_dir':'/data/tomcat/ejupay-mb-inrpc',
       'war_filename':'mb-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-mb-inrpc/webapps/mb-inrpc.war'
    },

'msg2-inrpc':
    {
       'group1':['10.20.1.5'],
       'group2':['10.20.1.6'],
       'groupfull':['10.20.1.5','10.20.1.6'],
       'port':8132,
       'instance_dir':'/data/tomcat/ejupay-msg2-inrpc',
       'war_filename':'msg2-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-msg2-inrpc/webapps/msg2-inrpc.war'
    },

'timer-inrpc':
    {
       'group1':['10.20.1.1'],
       'group2':['10.20.1.2'],
       'groupfull':['10.20.1.1','10.20.1.2'],
       'port':8133,
       'instance_dir':'/data/tomcat/ejupay-timer-inrpc',
       'war_filename':'timer-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-timer-inrpc/webapps/timer-inrpc.war'
    },

'access-outrpc':
    {
       'group1':['10.20.1.3'],
       'group2':['10.20.1.4'],
       'groupfull':['10.20.1.3','10.20.1.4'],
       'port':8135,
       'instance_dir':'/data/tomcat/ejupay-access-outrpc',
       'war_filename':'access-outrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-access-outrpc/webapps/access-outrpc.war'
    },

'channel-outrpc':
    {
       'group1':['10.20.1.5'],
       'group2':['10.20.1.6'],
       'groupfull':['10.20.1.5','10.20.1.6'],
       'port':8134,
       'instance_dir':'/data/tomcat/ejupay-channel-outrpc',
       'war_filename':'channel-outrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-channel-outrpc/webapps/channel-outrpc.war'
    },

'query-control':
    {
       'group1':['10.20.1.1'],
       'group2':['10.20.1.2'],
       'groupfull':['10.20.1.1','10.20.1.2'],
       'port':8136,
       'instance_dir':'/data/tomcat/ejupay-query-control',
       'war_filename':'query-control.war',
       'war_file_fullpath':'/data/tomcat/ejupay-query-control/webapps/query-control.war'
    },

'gateway-mock':
    {
       'group1':['10.20.1.3'],
       'group2':['10.20.1.4'],
       'groupfull':['10.20.1.3','10.20.1.4'],
       'port':8137,
       'instance_dir':'/data/tomcat/ejupay-gateway-mock',
       'war_filename':'gateway-mock.war',
       'war_file_fullpath':'/data/tomcat/ejupay-gateway-mock/webapps/gateway-mock.war'
    },

'access-pos':
    {
       'group1':['10.20.1.5'],
       'group2':['10.20.1.6'],
       'groupfull':['10.20.1.5','10.20.1.6'],
       'port':8138,
       'instance_dir':'/data/tomcat/ejupay-access-pos',
       'war_filename':'access-pos.war',
       'war_file_fullpath':'/data/tomcat/ejupay-access-pos/webapps/access-pos.war'
    },

'access-posfangjs':
    {
       'group1':['10.20.1.1'],
       'group2':['10.20.1.2'],
       'groupfull':['10.20.1.1','10.20.1.2'],
       'port':8139,
       'instance_dir':'/data/tomcat/ejupay-access-posfangjs',
       'war_filename':'access-posfangjs.war',
       'war_file_fullpath':'/data/tomcat/ejupay-access-posfangjs/webapps/access-posfangjs.war'
    },

'info-inrpc':
    {
       'group1':['10.20.1.3'],
       'group2':['10.20.1.4'],
       'groupfull':['10.20.1.3','10.20.1.4'],
       'port':8140,
       'instance_dir':'/data/tomcat/ejupay-info-inrpc',
       'war_filename':'info-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-info-inrpc/webapps/info-inrpc.war'
    },

'monitor-inrpc':
    {
       'group1':['10.20.1.5'],
       'group2':['10.20.1.6'],
       'groupfull':['10.20.1.5','10.20.1.6'],
       'port':8141,
       'instance_dir':'/data/tomcat/ejupay-monitor-inrpc',
       'war_filename':'monitor-inrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-monitor-inrpc/webapps/monitor-inrpc.war'
    },



'console-outrpc':
    {
       'group1':['10.20.1.1'],
       'group2':['10.20.1.2'],
       'groupfull':['10.20.1.1','10.20.1.2'],
       'port':8142,
       'instance_dir':'/data/tomcat/ejupay-console-outrpc',
       'war_filename':'console-outrpc.war',
       'war_file_fullpath':'/data/tomcat/ejupay-console-outrpc/webapps/console-outrpc.war'
    }




}
