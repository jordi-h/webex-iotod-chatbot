# Some Useful Commands

## Trim trailing spaces from each line, sort and remove duplicates.
```
awk '{ sub(/[ \t]+$/, ""); print }' filename.txt | sort | uniq > output.txt
```

## Regular expression that matches everything between \{ and | in a text
```
\{[^|]*\|
```

## Test my model in a python shell
See the Mindmeld documentation, I forgot.

## Count number of lines in code
find . \( -name '*.py' -o -name '*.yml' -o -name '*.sh' -o -name '*.dev' -o -name '*.env' \) -exec wc -l {} +

## to remove white lines and typo parentheses
^\s*\n
\(.*?\)
(?<=\{)[^|]+(?=\|)