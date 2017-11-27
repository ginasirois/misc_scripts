import os


# BASE Paths
CURR_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join('var', 'log', 'do160', 'txt')
DO160_DIR = os.path.join('opt', 'do160')
PROCESS_DIR = os.path.join(DO160_DIR, 'tools', 'process')
PSOC_DIR = os.path.join(DO160_DIR, 'PSoC_scripts')
BATS_DIR = os.path.join(DO160_DIR, 'bats')

# LOGFILE paths
WTF_LOG = os.path.join(LOG_DIR, 'wtf.txt')
VERSION_LOG = os.path.join(LOG_DIR, 'ac_version.txt')
VOLTAGE_LOG = os.path.join(LOG_DIR, 'voltages.txt')
A429_LOG = os.path.join(LOG_DIR, 'a429.txt')
ATP_LOG = os.path.join(LOG_DIR, 'ATP.txt')

# TEST script paths
GET_VERSION_SCRIPT = os.path.join(PSOC_DIR, 'psoc_get_version.sh')
GET_VOLTAGE_SCRIPT = os.path.join(PSOC_DIR, 'psoc_get_current_voltages.sh')
AC_VERSION_SCRIPT = os.path.join(PROCESS_DIR, 'ac-version.sh')
PSOC_VOLT_SCRIPT = os.path.join(PROCESS_DIR, 'psoc-volt.sh')
PROCESS_429_SCRIPT = os.path.join(PROCESS_DIR, 'process-a429.sh')
A429_TEST_SCRIPT = os.path.join(DO160_DIR, 'a429_test.sh')


# HELP file paths
HELP_DIR = os.path.join(CURR_DIR, 'help')
HELP_WTF = os.path.join(HELP_DIR, 'wtf.txt')
HELP_AC_VER = os.path.join(HELP_DIR, 'ac-vers.txt')
HELP_PSOC_VOLT = os.path.join(HELP_DIR, 'psoc-volt.txt')
HELP_429 = os.path.join(HELP_DIR, 'a429.txt')
HELP_ATP = os.path.join(HELP_DIR, 'ATP.txt')


# Command dictionary
RUN_CMD = [
    {
        'title': 'Run Wtf Cmd',
        'bash_cmd': ['ping', '8.8.8.8'],
 #      'bash_cmd': 'wtf | tee -a {0}; test -s {0};'.format(WTF_LOG),
    },
    {
        'title': 'Aircard Controller PSoc Ver',
        'bash_cmd': '{0} | tee -a {1}; {2}'.format(GET_VERSION_SCRIPT, VERSION_LOG, AC_VERSION_SCRIPT),
    },
    {
        'title': 'DC Voltage Check',
        'bash_cmd': '{0} | tee -a {1}; {2};'.format(GET_VOLTAGE_SCRIPT, VOLTAGE_LOG, PSOC_VOLT_SCRIPT),
    },
    {
        'title': 'ARINC429 Loopback Test',
        'bash_cmd': '{0} 3 | tee -a {1}; {2};'.format(A429_TEST_SCRIPT, A429_LOG, PROCESS_429_SCRIPT),
    },
    {
        'title': 'Run Automated ATP',
        'bash_cmd': '{0}/bin/bats {0}/demo.bats | tee -a ;'.format(BATS_DIR),
    },
    {
        'title': 'Help on Wtf Cmd',
        'bash_cmd': ['cat', '{0}'.format(HELP_WTF)],
    },
    {
        'title': 'Help on PSoc Ver',
        'bash_cmd': ['cat', '{0}'.format(HELP_AC_VER)],
    },
    {
        'title': 'Help on DC Voltage Test',
        'bash_cmd': ['cat', '{0}'.format(HELP_PSOC_VOLT)],
    },
    {
        'title': 'Help on A429 Loopback',
        'bash_cmd': ['cat', '{0}'.format(HELP_429)],
    },
    {
        'title': 'Help on ATP',
        'bash_cmd': ['cat', '{0}'.format(HELP_ATP)],
    },
    {
        'title': 'Exit',
        'bash_cmd': 'Q',
    },
    {
        'title': 'Back',
        'bash_cmd': 'Q'
    }
]

