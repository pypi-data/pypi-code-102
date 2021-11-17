from animalia import SpeciesNameGenerator
from appyratus.cli import (
    CliProgram,
    OptionalArg,
    PositionalArg,
)


class AnimaliaProgram(CliProgram):

    def args(self):
        return [
            PositionalArg(
                'action',
                usage='what do you want to do?',
                choices=['generate-species-name'],
            ),
            OptionalArg('count', default=1, dtype=int),
        ]


def execute_from_command_line():

    def call_action(program):
        cli_args = program.cli_args
        action = cli_args.action
        count = cli_args.count
        if action == 'generate-species-name':
            generator = SpeciesNameGenerator()
            names = generator.generate(count=count)
            for name in names:
                print(name)

    program = AnimaliaProgram(perform=call_action)
    program.run()


if __name__ == '__main__':
    main()
