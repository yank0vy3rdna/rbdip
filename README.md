# Photo Processor

## Диздок

Ссылка: https://docs.google.com/document/d/1pHrhBonUFVHa607quxPVimpAals6Qt1uiM6hlm4zO7Q/edit


### Localization (use Babel):

#### Command for create .mo file:

``` .\pybabel.exe extract ..\..\app\ -o ..\..\locale\base.pot ```
</br>
``` .\pybabel.exe init -l en ru -i ..\..\locale\base.pot -d ..\..\locale ```
</br>
``` .\pybabel.exe compile -d ..\..\locale\ ```

#### Command for update .po file:

``` .\pybabel.exe update -i ..\..\locale\base.pot -d ..\..\locale ```