"""
Expense Tracker Command

Provides CLI commands for tracking personal and project expenses with local JSON storage.
Supports adding, updating, deleting, listing, summarizing, and exporting expenses.
Includes optional monthly budget tracking with non-blocking warnings.
"""

import json
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import csv

import typer
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
app = typer.Typer(help="Track personal and project expenses")

# Configuration
DEVPULSE_DIR = Path.home() / ".devpulse"
EXPENSES_FILE = DEVPULSE_DIR / "expenses.json"
BUDGET_FILE = DEVPULSE_DIR / "budget.json"


# ================= Data Models =================

@dataclass
class Expense:
    """Represents a single expense."""
    amount: float
    category: str = "General"
    description: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Expense":
        """Create Expense from dictionary."""
        return Expense(**data)

    def get_month(self) -> str:
        """Extract YYYY-MM from timestamp."""
        return self.timestamp[:7]


@dataclass
class Budget:
    """Represents monthly budget configuration."""
    amount: float
    month: str  # YYYY-MM format

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Budget":
        return Budget(**data)


# ================= Storage Layer =================

class ExpenseStore:
    """Handles safe JSON read/write for expenses and budget."""

    @staticmethod
    def _ensure_dir() -> None:
        """Create ~/.devpulse directory if it doesn't exist."""
        DEVPULSE_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def load_expenses() -> List[Expense]:
        """Load expenses from JSON file. Returns empty list if file doesn't exist."""
        ExpenseStore._ensure_dir()
        if not EXPENSES_FILE.exists():
            return []
        try:
            with open(EXPENSES_FILE, "r") as f:
                data = json.load(f)
                return [Expense.from_dict(e) for e in data]
        except (json.JSONDecodeError, ValueError) as e:
            console.print(f"[yellow]⚠️  Warning: Could not read expenses file ({e}). Starting fresh.[/yellow]")
            return []

    @staticmethod
    def save_expenses(expenses: List[Expense]) -> None:
        """Save expenses to JSON file atomically."""
        ExpenseStore._ensure_dir()
        try:
            # Write to temp file first, then rename (atomic operation)
            temp_file = EXPENSES_FILE.with_suffix(".tmp")
            with open(temp_file, "w") as f:
                json.dump([e.to_dict() for e in expenses], f, indent=2)
            temp_file.replace(EXPENSES_FILE)
        except IOError as e:
            console.print(f"[red]✗ Error saving expenses: {e}[/red]")
            raise

    @staticmethod
    def load_budget(month: str) -> Optional[Budget]:
        """Load budget for a specific month."""
        ExpenseStore._ensure_dir()
        if not BUDGET_FILE.exists():
            return None
        try:
            with open(BUDGET_FILE, "r") as f:
                budgets = json.load(f)
                for b in budgets:
                    if b.get("month") == month:
                        return Budget.from_dict(b)
                return None
        except (json.JSONDecodeError, ValueError):
            console.print("[yellow]⚠️  Warning: Could not read budget file. Starting fresh.[/yellow]")
            return None

    @staticmethod
    def save_budget(budget: Budget) -> None:
        """Save or update budget for a specific month."""
        ExpenseStore._ensure_dir()
        try:
            # Load existing budgets
            budgets = []
            if BUDGET_FILE.exists():
                try:
                    with open(BUDGET_FILE, "r") as f:
                        budgets = json.load(f)
                except json.JSONDecodeError:
                    budgets = []
            
            # Update or add the budget for this month
            budgets = [b for b in budgets if b.get("month") != budget.month]
            budgets.append(budget.to_dict())
            
            # Write atomically
            temp_file = BUDGET_FILE.with_suffix(".tmp")
            with open(temp_file, "w") as f:
                json.dump(budgets, f, indent=2)
            temp_file.replace(BUDGET_FILE)
        except IOError as e:
            console.print(f"[red]✗ Error saving budget: {e}[/red]")
            raise


# ================= Business Logic =================

class ExpenseManager:
    """Business logic for expense operations."""

    @staticmethod
    def add_expense(amount: float, category: str = "General", description: str = "") -> Expense:
        """Add a new expense and check budget."""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        expense = Expense(amount=amount, category=category, description=description)
        expenses = ExpenseStore.load_expenses()
        expenses.append(expense)
        ExpenseStore.save_expenses(expenses)
        
        # Check budget
        ExpenseManager._check_budget(expense.get_month())
        
        return expense

    @staticmethod
    def update_expense(expense_id: str, amount: Optional[float] = None, 
                       category: Optional[str] = None, description: Optional[str] = None) -> Expense:
        """Update an existing expense."""
        expenses = ExpenseStore.load_expenses()
        expense = None
        for e in expenses:
            if e.id == expense_id:
                expense = e
                break
        
        if expense is None:
            raise ValueError(f"Expense with ID '{expense_id}' not found")
        
        if amount is not None:
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            expense.amount = amount
        if category is not None:
            expense.category = category
        if description is not None:
            expense.description = description
        
        ExpenseStore.save_expenses(expenses)
        ExpenseManager._check_budget(expense.get_month())
        
        return expense

    @staticmethod
    def delete_expense(expense_id: str) -> bool:
        """Delete an expense by ID. Returns True if deleted, False if not found."""
        expenses = ExpenseStore.load_expenses()
        original_len = len(expenses)
        expenses = [e for e in expenses if e.id != expense_id]
        
        if len(expenses) == original_len:
            return False
        
        ExpenseStore.save_expenses(expenses)
        return True

    @staticmethod
    def list_expenses(month: Optional[str] = None, category: Optional[str] = None) -> List[Expense]:
        """List expenses with optional filters."""
        expenses = ExpenseStore.load_expenses()
        
        if month:
            expenses = [e for e in expenses if e.get_month() == month]
        
        if category:
            expenses = [e for e in expenses if e.category.lower() == category.lower()]
        
        return sorted(expenses, key=lambda e: e.timestamp, reverse=True)

    @staticmethod
    def get_summary(month: Optional[str] = None) -> Dict:
        """Get summary of expenses by month and category."""
        expenses = ExpenseStore.load_expenses()
        
        if month:
            expenses = [e for e in expenses if e.get_month() == month]
        
        summary = {
            "total": 0,
            "by_category": {},
            "months": {}
        }
        
        for expense in expenses:
            summary["total"] += expense.amount
            
            # By category
            if expense.category not in summary["by_category"]:
                summary["by_category"][expense.category] = 0
            summary["by_category"][expense.category] += expense.amount
            
            # By month
            month_key = expense.get_month()
            if month_key not in summary["months"]:
                summary["months"][month_key] = {"total": 0, "count": 0}
            summary["months"][month_key]["total"] += expense.amount
            summary["months"][month_key]["count"] += 1
        
        return summary

    @staticmethod
    def _check_budget(month: str) -> None:
        """Check if expenses exceed budget for the month and warn if needed."""
        budget = ExpenseStore.load_budget(month)
        if not budget:
            return
        
        month_expenses = ExpenseManager.list_expenses(month=month)
        total = sum(e.amount for e in month_expenses)
        
        if total > budget.amount:
            percentage = (total / budget.amount) * 100
            console.print(f"[yellow]⚠️  Budget alert: ${total:.2f} spent, budget is ${budget.amount:.2f} ({percentage:.0f}%)[/yellow]")

    @staticmethod
    def set_budget(amount: float, month: str) -> Budget:
        """Set a monthly budget."""
        if amount < 0:
            raise ValueError("Budget amount cannot be negative")
        
        budget = Budget(amount=amount, month=month)
        ExpenseStore.save_budget(budget)
        return budget

    @staticmethod
    def export_to_csv(filepath: str, month: Optional[str] = None, category: Optional[str] = None) -> None:
        """Export expenses to CSV file."""
        expenses = ExpenseManager.list_expenses(month=month, category=category)
        
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Amount", "Category", "Description", "Timestamp"])
                for e in expenses:
                    writer.writerow([e.id, e.amount, e.category, e.description, e.timestamp])
            console.print(f"[green]✓ Exported {len(expenses)} expenses to {filepath}[/green]")
        except IOError as e:
            console.print(f"[red]✗ Error exporting to CSV: {e}[/red]")
            raise


# ================= CLI Commands =================

@app.command()
def add(
    amount: float = typer.Argument(..., help="Amount spent (required)"),
    category: str = typer.Option("General", "--category", "-c", help="Expense category"),
    description: str = typer.Option("", "--description", "-d", help="Short description"),
):
    """Add a new expense."""
    try:
        expense = ExpenseManager.add_expense(amount, category, description)
        console.print(f"[green]✓ Expense added[/green] (ID: {expense.id})")
        console.print(f"  Amount: ${expense.amount:.2f}")
        console.print(f"  Category: {expense.category}")
        if expense.description:
            console.print(f"  Description: {expense.description}")
    except ValueError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def update(
    expense_id: str = typer.Argument(..., help="Expense ID to update"),
    amount: Optional[float] = typer.Option(None, "--amount", "-a", help="New amount"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="New category"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description"),
):
    """Update an existing expense."""
    try:
        expense = ExpenseManager.update_expense(expense_id, amount, category, description)
        console.print(f"[green]✓ Expense updated[/green] (ID: {expense.id})")
        console.print(f"  Amount: ${expense.amount:.2f}")
        console.print(f"  Category: {expense.category}")
    except ValueError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def delete(
    expense_id: str = typer.Argument(..., help="Expense ID to delete"),
):
    """Delete an expense."""
    try:
        if ExpenseManager.delete_expense(expense_id):
            console.print(f"[green]✓ Expense deleted[/green] (ID: {expense_id})")
        else:
            console.print(f"[red]✗ Expense with ID '{expense_id}' not found[/red]")
            raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def list(
    month: Optional[str] = typer.Option(None, "--month", "-m", help="Filter by month (YYYY-MM)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
):
    """List all expenses with optional filters."""
    try:
        expenses = ExpenseManager.list_expenses(month=month, category=category)
        
        if not expenses:
            console.print("[dim]No expenses found.[/dim]")
            return
        
        table = Table(title="Expenses", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Category", style="magenta")
        table.add_column("Description", style="white")
        table.add_column("Date", style="dim")
        
        for e in expenses:
            date_str = datetime.fromisoformat(e.timestamp).strftime("%Y-%m-%d %H:%M")
            table.add_row(e.id, f"${e.amount:.2f}", e.category, e.description, date_str)
        
        console.print(table)
        console.print(f"\n[bold]Total: ${sum(e.amount for e in expenses):.2f}[/bold]")
    
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def summary(
    month: Optional[str] = typer.Option(None, "--month", "-m", help="Summary for specific month (YYYY-MM)"),
):
    """Show expense summary by month and category."""
    try:
        data = ExpenseManager.get_summary(month=month)
        
        if data["total"] == 0:
            console.print("[dim]No expenses found.[/dim]")
            return
        
        # Summary by category
        if data["by_category"]:
            table = Table(title="Summary by Category", box=box.ROUNDED)
            table.add_column("Category", style="magenta")
            table.add_column("Amount", justify="right", style="green")
            table.add_column("Percentage", justify="right", style="cyan")
            
            for category, amount in sorted(data["by_category"].items(), key=lambda x: x[1], reverse=True):
                pct = (amount / data["total"]) * 100 if data["total"] > 0 else 0
                table.add_row(category, f"${amount:.2f}", f"{pct:.1f}%")
            
            console.print(table)
        
        # Monthly summary
        if data["months"]:
            table = Table(title="Summary by Month", box=box.ROUNDED)
            table.add_column("Month", style="cyan")
            table.add_column("Total", justify="right", style="green")
            table.add_column("Count", justify="right", style="yellow")
            table.add_column("Budget Status", style="white")
            
            for month_key in sorted(data["months"].keys(), reverse=True):
                month_data = data["months"][month_key]
                budget = ExpenseStore.load_budget(month_key)
                status = "[dim]No budget[/dim]"
                if budget:
                    pct = (month_data["total"] / budget.amount) * 100
                    if month_data["total"] > budget.amount:
                        status = f"[red]${month_data['total']:.2f} / ${budget.amount:.2f} ({pct:.0f}%)[/red]"
                    else:
                        remaining = budget.amount - month_data["total"]
                        status = f"[green]${month_data['total']:.2f} / ${budget.amount:.2f} (${remaining:.2f} left)[/green]"
                
                table.add_row(month_key, f"${month_data['total']:.2f}", str(month_data["count"]), status)
            
            console.print(table)
        
        console.print(f"\n[bold]Total Spent: ${data['total']:.2f}[/bold]")
    
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def export(
    output: str = typer.Option("expenses.csv", "--output", "-o", help="Output CSV file path"),
    month: Optional[str] = typer.Option(None, "--month", "-m", help="Filter by month (YYYY-MM)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
):
    """Export expenses to CSV file."""
    try:
        ExpenseManager.export_to_csv(output, month=month, category=category)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def set_budget(
    amount: float = typer.Argument(..., help="Monthly budget amount"),
    month: Optional[str] = typer.Option(None, "--month", "-m", help="Month (YYYY-MM, defaults to current)"),
):
    """Set a monthly budget."""
    try:
        if not month:
            month = datetime.now().strftime("%Y-%m")
        
        budget = ExpenseManager.set_budget(amount, month)
        console.print(f"[green]✓ Budget set for {month}[/green]")
        console.print(f"  Amount: ${budget.amount:.2f}")
        
        # Show current spending for this month
        month_expenses = ExpenseManager.list_expenses(month=month)
        total = sum(e.amount for e in month_expenses)
        if total > 0:
            pct = (total / budget.amount) * 100
            remaining = budget.amount - total
            console.print(f"  Current spending: ${total:.2f} ({pct:.1f}% of budget)")
            console.print(f"  Remaining: ${remaining:.2f}")
    
    except ValueError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(code=1)
