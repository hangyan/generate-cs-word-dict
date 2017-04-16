# generate-cs-word-dict

When use some editors/IDEs(emacs, pycharm for example) which support spell check, we need to frequently 
add some 'custom` word to silent the warnings. Since these words are mainly 'programming terminology', it 
would be great if there are some exist dict for this purpose. I'dont have the luck to find one, so i choose 
to generate one from the tag list of stackoverflow. [link](http://stackoverflow.com/tags?page=1&tab=popular)


Feel free to download this `dict` file and use.


## Emacs ispell settings

```
cp dict ~/.emacs.d/ispell_english


;; emacs settings
(setq ispell-program-name "/usr/local/bin/ispell")
(setq ispell-personal-dictionary "~/.emacs.d/ispell_english")
```

## Pycharm

`Editor -> Spelling -> Dictionaries`


