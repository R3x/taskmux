# taskmux

Using tmux to run tasks in parallel - useful for quick experiments and stuff

## Config file

```yaml
jobs:
  - name: job1 # will also be the name of the session
    matrix_type: 1D
    matrix: 
        ID : [1, 2, 3]  # Each command will get one value
        VAL : ["AAAA", "BBB", "CCCC"]
    commands:
        - echo "ID : ${ID}"
        - echo "VAL : ${VAL}"
  - name: job2
    matrix_type: 2D
    matrix:
        T1 : ["A", "B"]
        T2 : ["X", "Y"]
    commands:
        - echo "${T1}:${T2}"
  - name: job3
    instances: 4
    commands:
        - echo "Hello"
        - echo "World" 
```

Here, `job1` will run 3 commands in parallel, each with a different value of `ID` and `VAL`.
    - echo "ID : 1"
    - echo "VAL : AAAA"

    - echo "ID : 2"
    - echo "VAL : BBB"

    - echo "ID : 3"
    - echo "VAL : CCCC"
In 3 different panes of the session named `job1`.

Similarly, `job2` will run 4 commands in parallel, each with a different value of `T1` and `T2`. 
    - echo "A:X"
    - echo "A:Y"
    - echo "B:X"
    - echo "B:Y"
In 4 different panes of the session named `job2`.

Finally, `job3` will run 4 commands in parallel, each with the same command.
    - echo "Hello"
    - echo "World"
In 4 different panes of the session named `job3`.