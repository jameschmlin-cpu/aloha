
def log_failure(component, error_code):
    with open(r'C:\Genesis\activity.log', 'a') as f:
        f.write(f'FAIL:{component}:{error_code}\n')
