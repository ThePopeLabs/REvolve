import pytest
from unittest import mock
from revolve.architectures.strategies import MLPStrategy, Conv2DStrategy
from revolve.architectures.chromosomes import MLPChromosome, Conv2DChromosome
from revolve.architectures.genes import FCGene, ParameterGene, Conv2DGene


@pytest.mark.parametrize(
    "strategy, params, strategy_params",
    [
        (
            MLPStrategy,
            "mlp_params",
            {
                "max_fc": 1,
                "squeeze_fc": True,
                "epochs": 10,
                "callback": mock.MagicMock(),
                "loss": "mean_squared_error",
                "metric": "mean_absolute_error",
            },
        ),
        (
            MLPStrategy,
            "mlp_params",
            {
                "max_fc": 1,
                "squeeze_fc": True,
                "epochs": 10,
                "callback": mock.MagicMock(),
                "loss": mock.MagicMock(),
                "metric": mock.MagicMock(),
            },
        ),
        (
            Conv2DStrategy,
            "conv_network_params",
            {
                "max_fc": 1,
                "squeeze_fc": True,
                "max_conv": 1,
                "expand_conv": True,
                "epochs": 10,
                "callback": mock.MagicMock(),
                "loss": mock.MagicMock(),
                "metric": mock.MagicMock(),
            },
        ),
        (
            Conv2DStrategy,
            "conv_network_params",
            {
                "max_fc": 1,
                "squeeze_fc": True,
                "max_conv": 1,
                "expand_conv": True,
                "epochs": 10,
                "callback": mock.MagicMock(),
                "loss": "mean_squared_error",
                "metric": "mean_absolute_error",
            },
        ),
    ],
)
def test_strategy_init(strategy, params, strategy_params, request):
    params = request.getfixturevalue(params)
    strategy = strategy(parameters=params, **strategy_params)
    for key in strategy.__dict__.keys():
        if key == "parameters":
            assert isinstance(getattr(strategy, key), dict)
        elif key == "loss" or "metric":
            assert getattr(strategy, key) == strategy_params[key] or mock.MagicMock()
        else:
            assert getattr(strategy, key) == strategy_params[key]


@pytest.mark.parametrize(
    "strategy, chromosome_genes, expected_chromosome",
    [
        ("mlp_strategy", "mlp_chromosome_genes", MLPChromosome),
        ("conv2d_strategy", "conv_chromosome_genes", Conv2DChromosome),
    ],
)
def test_create_new_chromosome(
    strategy, chromosome_genes, expected_chromosome, request
):
    strategy = request.getfixturevalue(strategy)
    chromosome_genes = request.getfixturevalue(chromosome_genes)
    new_chromosome = strategy.create_new_chromosome(genes=chromosome_genes)
    assert isinstance(new_chromosome, expected_chromosome)


@pytest.mark.parametrize(
    "strategy, parameters, param",
    [
        ("mlp_strategy", "mlp_params", "batch_size"),
        ("mlp_strategy", "mlp_params", "regression_activation"),
        ("conv2d_strategy", "conv_network_params", "batch_size"),
        ("conv2d_strategy", "conv_network_params", "regression_activation"),
    ],
)
def test_parameter_choice(strategy, parameters, param, request):
    strategy = request.getfixturevalue(strategy)
    parameters = request.getfixturevalue(parameters)
    chosen_param = strategy.parameter_choice(parameters, param)
    assert chosen_param in strategy.parameters.get(param)


@pytest.mark.parametrize(
    "strategy, population_size, expected_population_size, expected_genes, expected_chromosome",
    [
        (
            "mlp_strategy",
            100,
            100,
            (FCGene, ParameterGene),
            MLPChromosome,
        ),  # Test with valid input
        (
            "mlp_strategy",
            0,
            0,
            (FCGene, ParameterGene),
            MLPChromosome,
        ),  # Test with input 0
        (
            "conv2d_strategy",
            100,
            100,
            (Conv2DGene, FCGene, ParameterGene),
            Conv2DChromosome,
        ),  # Test with valid input
        (
            "conv2d_strategy",
            0,
            0,
            (Conv2DGene, FCGene, ParameterGene),
            Conv2DChromosome,
        ),  # Test with input 0
    ],
)
def test_generate_population(
    strategy,
    population_size,
    expected_population_size,
    expected_genes,
    expected_chromosome,
    request,
):
    strategy = request.getfixturevalue(strategy)
    population = strategy.generate_population(population_size)
    assert len(population) == expected_population_size
    for chromosome in population:
        assert isinstance(chromosome, expected_chromosome)
        for gene in chromosome.genes:
            assert isinstance(gene, expected_genes)
