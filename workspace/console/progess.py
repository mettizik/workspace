"""
Utils to write down progress of the long operation
"""


class ProgressWriter:
    """
    Base class for progress outputing
    """

    def __init__(self, write_function=print, format_string='\r{current} of {total}', **write_function_kwargs):
        self._print = write_function
        self._format = format_string
        self._write_additional_args = write_function_kwargs

    def _prepare(self):
        self._print('\n')
    
    def __del__(self):
        self._print('\n')

    def display_progress(self, observer):
        self._print(
            self._format.format(
                current=observer._get_current(),
                total=observer._get_total()),
                **self._write_additional_args)

class PercentsWriter(ProgressWriter):
    """
    Progress writer, that enables percentage output of progress
    """

    def __init__(self, write_function=print, format_string='\r{percents:>3d} %', **write_function_kwargs):
        ProgressWriter.__init__(self, write_function,
                                format_string,
                                **write_function_kwargs)

    def display_progress(self, observer):
        total = observer._get_total() if observer._get_total() != 0 else observer._get_current()
        percentage = int(observer._get_current() / total * 100) 
        self._print(self._format.format(percents=percentage), **self._write_additional_args)

class ProgressObserver:
    """
    Base class to implement obsevation of the progress change    
    """

    def __init__(self, total, current=0, printer=ProgressWriter(end=''), display_on_init=True):        
        """
        Create progress observer for some operation
            * total     - count of total steps expected during operation
            * current   - starting state of observer
            * printer   - a sub-class of the ProgressWriter to display progress
            * display_on_init - display initial state after creation
        """
        self._printer = printer        
        self.reset(total, current, display_on_init)
        
    def _prepare(self):
        if not self._ready:
            self._printer._prepare()
            self._ready = True

    def _get_current(self):
        return self._current

    def _get_total(self):
        return self._total

    def update(self, delta=1):
        """
        Update state of observer, due to progress change
            * delta - change of the progress value to display
        """
        self._current += delta
        self._prepare()
        self._printer.display_progress(self)


    def reset(self, total, current=0, display_now=True):
        """
        Resets state of tehe progress observer for the new operation
            * total     - count of total steps expected during operation
            * current   - starting state of observer
            * display_now - display new state after reset
        """        
        self._current = current
        self._total = total
        self._ready = False
        if display_now:
            self._prepare()

class AccumulatorObserver(ProgressObserver):
    """
    Observer implementation for operations with undefined count of steps, e.g. reading data from socket
    """
    def __init__(self, _current=0, _printer=ProgressWriter(format_string='\r{current} ...', end=''), _display_on_init=True):
        ProgressObserver.__init__(self, total=0, current=_current, printer=_printer, display_on_init=_display_on_init)
