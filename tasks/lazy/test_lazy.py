import Task from .

def test_lazy():
    input = read_test_csv('./test_data/input.csv')
    expected = read_test_csv('./test_data/output.csv')

    output = Task(
        inputs={
            'events': input,
        }
    )

    assert output == expected