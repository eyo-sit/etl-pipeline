from connect import connect
from soda.scan import Scan

if __name__ == '__main__':
    conn = connect()
    cursor = conn.cursor()
    
    scan = Scan()
    scan.set_data_source_name("events")

    # Add configuration YAML files
    #########################
    # Choose one of the following to specify data source connection configurations :
    # 1) From a file
    scan.add_configuration_yaml_file(file_path="./soda/configuration.yml")

    # Execute the scan
    ##################
    scan.execute()

    # Set logs to verbose mode, equivalent to CLI -V option
    ##################
    scan.set_verbose(True)

    # Set scan definition name, equivalent to CLI -s option;
    # see Tips and best practices below
    ##################
    scan.set_scan_definition_name("YOUR_SCHEDULE_NAME")


    # Inspect the scan result
    #########################
    scan.get_scan_results()

    # Inspect the scan logs
    #######################
    scan.get_logs_text()

    # Typical log inspection
    ##################
    scan.assert_no_error_logs()
    scan.assert_no_checks_fail()

    # Advanced methods to inspect scan execution logs
    #################################################
    scan.has_error_logs()
    scan.get_error_logs_text()

    # Advanced methods to review check results details
    ########################################
    scan.get_checks_fail()
    scan.has_check_fails()
    scan.get_checks_fail_text()
    scan.assert_no_checks_warn_or_fail()
    scan.get_checks_warn_or_fail()
    scan.has_checks_warn_or_fail()
    scan.get_checks_warn_or_fail_text()
    scan.get_all_checks_text()
