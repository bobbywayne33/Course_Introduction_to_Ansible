#!/usr/bin/python

from ansible.module_utils.basic import *
import winrm

def run_module():
    module_args = dict(
        host=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        port=dict(type='int', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(changed=False)

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    try:
        session = winrm.Session(module.params['host'], auth=(module.params['username'], module.params['password']))
        ps_script = """
        $ErrorActionPreference = "Stop"
        cd WSMan:\localhost\Plugin\Microsoft.WSMan.Management\Service\DefaultPorts
        New-Item -Name "Custom" -Value @{Transport="HTTP"; Port="{}"}
        """.format(module.params['port'])
        session.run_ps(ps_script)
        result['changed'] = True
        result['message'] = 'WMI endpoint created successfully'
    except Exception as e:
        module.fail_json(msg='Failed to create WMI endpoint: %s' % to_native(e), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
