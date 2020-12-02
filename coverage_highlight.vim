" The main entry point of our VIM stuff. We add a hook for when every file is
" read, eg, `BufWinEnter *.*`
"
" Just put the `coverage_parser.py` and `coverage_highlight.vim` into
" `~/.vim/plugin`

" Save the CPO
let s:cpo_save = &cpo
set cpo&vim

" Check that we have python3 support compiled into VIM
if !has('python3')
    echo "For the coverage_highlight plugin to work, VIM must be configured with python3 support"
else
	" Define the colors to use for covered and uncovered lines Effectively for
	" 256-color terminals, colors 232 through 255 are very dark greys
	" rgb(8,8,8), through nearly white rgb(238,238,238), in rgb(10,10,10)
	" increments
	" This might require that you have TERM=xterm-256color _shrug_
	highlight CoveredLineColor ctermbg=233

	" Define the sign we will use for covered lines
	execute 'sign define covered_line_color linehl=CoveredLineColor'

	" Load the python file we actually implement the parser and highlighting in
	py3file <sfile>:p:h/coverage_parser.py

	" Create a function which will be invoked upon our auto group
	function! s:startup() abort
		" Just invoke our python plugin code
  		python3 coverage_highlight()
	endfunction

	" Register an auto group for when a file has been loaded, this will cause
	" the `s:startup()` function to get invoked every time you finish reading
	" a file in VIM
	augroup coverage_highlight_augroup
		autocmd BufWinEnter *.* call s:startup()
	augroup END
end

" Restore the CPO
let &cpo = s:cpo_save
unlet s:cpo_save

