"""
RepoMind AI Command Line Interface.
"""

import argparse

from src.services.rag_service import RAGService
from src.services.repository_intelligence import RepositoryIntelligence
from src.services.code_graph_service import CodeGraphService
from src.services.architecture_service import ArchitectureService
from src.services.report_service import ReportService
from src.services.documentation_service import DocumentationService
from src.services.explain_service import ExplainService
from src.services.review_service import ReviewService
from src.services.stats_service import StatsService
from src.services.dependency_service import DependencyService
from src.services.search_service import SearchService


def analyze_repository(path: str):

    intelligence = RepositoryIntelligence()

    result = intelligence.analyze(path)

    print("\n===== RepoMind AI Analysis =====\n")

    print(result)


def ask_repository(question: str):

    rag = RAGService()

    answer = rag.ask(question)

    print("\n===== RepoMind AI Answer =====\n")

    print(answer)


def map_repository(path: str):

    service = CodeGraphService()

    graph = service.generate_graph(path)

    diagram = service.generate_mermaid(graph)

    print("\n===== Repository Map =====\n")

    print(diagram)


def architecture_repository(path: str):

    service = ArchitectureService()

    architecture = service.analyze_structure(path)

    print("\n===== Repository Architecture =====\n")

    print(service.generate_architecture_summary(architecture))


def report_repository(path: str):

    service = ReportService()

    print("\n===== RepoMind AI Report =====\n")

    print(service.generate_report(path))


def docs_repository(path: str):

    service = DocumentationService()

    result = service.generate(path)

    print("\n===== Documentation Generated =====\n")

    print(result)


def explain_file(path: str):

    service = ExplainService()

    print("\n===== File Explanation =====\n")

    print(service.explain(path))


def review_repository(path: str):

    service = ReviewService()

    result = service.generate_review(repository_name=path)

    print("\n===== Repository Review =====\n")

    print(result)


def stats_repository(path: str):

    service = StatsService()

    result = service.generate_statistics(path)

    print("\n===== Repository Statistics =====\n")

    print(result)


def deps_repository(path: str):

    service = DependencyService()

    result = service.analyze(path)

    print("\n===== Dependency Analysis =====\n")

    for file, imports in result.items():

        print(f"\n{file}")

        if imports:

            for item in imports:

                print(f"  -> {item}")

        else:

            print("  (no imports)")


def search_repository(query: str):

    service = SearchService()

    results = service.search(query)

    print("\n===== Semantic Search Results =====\n")

    for index, item in enumerate(results, start=1):

        metadata = item.get("metadata", {})

        print(f"{index}. {metadata.get('file', 'unknown')}")

        print(metadata.get("content", "")[:300])

        print("\n--------------------\n")


def main():

    parser = argparse.ArgumentParser(description="RepoMind AI CLI")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    analyze_parser = subparsers.add_parser("analyze", help="Analyze repository")

    analyze_parser.add_argument("path")

    ask_parser = subparsers.add_parser("ask", help="Ask questions about repository")

    ask_parser.add_argument("question")

    map_parser = subparsers.add_parser("map", help="Generate repository map")

    map_parser.add_argument("path")

    architecture_parser = subparsers.add_parser(
        "architecture", help="Analyze architecture"
    )

    architecture_parser.add_argument("path")

    report_parser = subparsers.add_parser("report", help="Generate report")

    report_parser.add_argument("path")

    docs_parser = subparsers.add_parser("docs", help="Generate documentation")

    docs_parser.add_argument("path")
    explain_parser = subparsers.add_parser("explain", help="Explain a Python file")

    explain_parser.add_argument("path")

    review_parser = subparsers.add_parser("review", help="Review repository")

    review_parser.add_argument("path")

    stats_parser = subparsers.add_parser("stats", help="Repository statistics")

    stats_parser.add_argument("path")

    search_parser = subparsers.add_parser("search", help="Semantic repository search")

    search_parser.add_argument("query")
    deps_parser = subparsers.add_parser("deps", help="Repository dependencies")

    deps_parser.add_argument("path")

    args = parser.parse_args()

    if args.command == "analyze":

        analyze_repository(args.path)

    elif args.command == "ask":

        ask_repository(args.question)

    elif args.command == "map":

        map_repository(args.path)

    elif args.command == "architecture":

        architecture_repository(args.path)

    elif args.command == "report":

        report_repository(args.path)

    elif args.command == "docs":

        docs_repository(args.path)

    elif args.command == "review":

        review_repository(args.path)

    elif args.command == "explain":

        explain_file(args.path)

    elif args.command == "stats":

        stats_repository(args.path)

    elif args.command == "deps":

        deps_repository(args.path)

    elif args.command == "search":

        search_repository(args.query)


if __name__ == "__main__":
    main()
