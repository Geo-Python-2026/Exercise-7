from points_decorator import points
import inspect
import pandas as pd

class TestProblem1:
    @points(0.5, "Problem 1, Part 1: Did you create a dataframe `data` with 1000 random values?")
    def test_problem_1_part_1(self, problem1):
        section_data, namespace = problem1
        section = "Part 1"
        variables = section_data[section]['variables']

        assert isinstance(variables['data'], pd.DataFrame)
        assert len(variables['data']) == 1000

    @points(0.5, "Problem 1, Part 2: Did you create 1000 random values for colors?")
    def test_problem_1_part_2(self, problem1):
        section_data, namespace = problem1
        section = "Part 2"  # Define the section key
        variables = section_data[section]['variables']

        assert len(variables['colors']) == 1000
        assert type(variables['colors'][0]) == float

    @points(1, "Problem 1, Part 3: Did you add a title to your plot?")
    def test_problem_1_part_3_title(self, problem1):
        section_data, namespace = problem1
        section = "Part 3"  # Define the section key
        variables = section_data[section]['variables']

        assert 'title' in variables
        
    
    @points(0.5, "Problem 1, Part 3: Did you add an x-label to your plot?")
    def test_problem_1_part_3_xlabel(self, problem1):
        section_data, namespace = problem1
        section = "Part 3"  # Define the section key
        variables = section_data[section]['variables']

        assert 'xlabel' in variables

    @points(0.5, "Problem 1, Part 3: Did you add an y-label to your plot?")
    def test_problem_1_part_3_ylabel(self, problem1):
        section_data, namespace = problem1
        section = "Part 3"  # Define the section key
        variables = section_data[section]['variables']

        assert 'ylabel' in variables
