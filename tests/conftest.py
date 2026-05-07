from src.logger.setup_logger import setup_logger

_test_progress = {}

def pytest_collection_modifyitems(session, config, items):
    """Inicializa el seguimiento de progreso para cada archivo de test."""
    global _test_progress
    _test_progress = {}
    
    for item in items:
        # Extraer nombre del archivo sin extensión
        module = item.nodeid.split('::')[0].split('/')[-1].replace('.py', '')
        if module not in _test_progress:
            _test_progress[module] = {
                'logger': setup_logger(name=module, log_to_file=True),
                'total': 0,
                'completed': 0,
                'logged_25': False,
                'logged_50': False,
                'logged_75': False
            }
        _test_progress[module]['total'] += 1

def pytest_runtest_logreport(report):
    """Registra el progreso después de cada test."""
    if report.when == 'call' and report.outcome in ('passed', 'failed', 'skipped'):
        module = report.nodeid.split('::')[0].split('/')[-1].replace('.py', '')
        if module in _test_progress:
            _test_progress[module]['completed'] += 1
            total = _test_progress[module]['total']
            completed = _test_progress[module]['completed']
            
            if total > 0:
                percent = int((completed / total) * 100)
                logger = _test_progress[module]['logger']
                
                if percent >= 25 and not _test_progress[module]['logged_25']:
                    logger.info(f"PROGRESS | 25% completed ({completed}/{total})")
                    _test_progress[module]['logged_25'] = True
                if percent >= 50 and not _test_progress[module]['logged_50']:
                    logger.info(f"PROGRESS | 50% completed ({completed}/{total})")
                    _test_progress[module]['logged_50'] = True
                if percent >= 75 and not _test_progress[module]['logged_75']:
                    logger.info(f"PROGRESS | 75% completed ({completed}/{total})")
                    _test_progress[module]['logged_75'] = True
                if percent >= 100:
                    logger.info(f"PROGRESS | 100% completed ({completed}/{total})")
