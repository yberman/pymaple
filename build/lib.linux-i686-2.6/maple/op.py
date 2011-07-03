from core import Proxy
 
# misc
modop = Proxy('`mod`')
fatop = Proxy('`!`')
dollarop = Proxy('`$`')
ditto1 = Proxy('`%`')
ditto2 = Proxy('`%%`')
ditto3 = Proxy('`%%%`')
atop = Proxy('`@`')
atatop = Proxy('`@@`')
neutralop = Proxy('`&`')
neutral = lambda x: Proxy('`&%s`' % x)
setop = Proxy('`{}`')
listlop = Proxy('`[]`')
catop = Proxy('`||`')

# arithmetic
mulop = Proxy('`*`')
addop = Proxy('`+`')
subop = Proxy('`-`')
dotop = Proxy('`.`')
divop = Proxy('`/`')
powop = Proxy('`**`')
hatop = Proxy('`^`')

# relations
ltop = Proxy('`<`')
leop = Proxy('`<=`')
neop = Proxy('`<>`')
neop = Proxy('`<>`')
eqop = Proxy('`=`')
gtop = Proxy('`>`')
geop = Proxy('`>=`')

# logical
andop = Proxy('`and`')
orop = Proxy('`or`')
xorop = Proxy('`xor`')
impliesop = Proxy('`implies`')
notop = Proxy('`not`')

# set
unionop = Proxy('`union`')
intersectop = Proxy('`intersect`')
minusop = Proxy('`minus`')
subsetop = Proxy('`subset`')
inop = Proxy('`in`')