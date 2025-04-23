from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from trading_analysis.tools.calculator_tool import CalculatorTool
# from trading_analysis.tools.sec_tools import SEC10KTool, SEC10QTool

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool, FileReadTool
from trading_analysis.tools.execution_tool import ExecutionTool
from trading_analysis.tools.portfolio_tool import PortfolioTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TradingAnalysis():
    """TradingAnalysis crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[
                WebsiteSearchTool(),
                ScrapeWebsiteTool(),
                TXTSearchTool()
            ],
            verbose=True
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            tools=[
                WebsiteSearchTool(),
                ScrapeWebsiteTool(),
                TXTSearchTool(),
                ExecutionTool(),
                FileReadTool(file_path='report.md'),
                PortfolioTool(),
                # CalculatorTool(),
                # SEC10KTool(),
                # SEC10QTool(),
            ],
            callback_agent=self.researcher,
            verbose=True
        )
    # @agent
    # def news_monitor(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['news_monitor'],
    #         tools=[
    #             WebsiteSearchTool(),
    #             ScrapeWebsiteTool(),
    #             TXTSearchTool(),
    #         ],
    #         verbose=True
    #     )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )
    
    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='data/report.md'
        )
    
    @task
    def market_data_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_data_analysis_task'],
        )
    
    @task
    def strategy_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['strategy_validation_task'],
            output_file='data/strategy_validation_report.md',
        )
    
    @task
    def deep_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['deep_research_task'],
            output_file='data/deep_research_report.md',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TradingAnalysis crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
