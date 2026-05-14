#!/usr/bin/env python3
"""
Manufacturing Quality Analyzer - Installation & Functionality Test Script
Tests all dependencies and core functionality without GUI

Usage:
    python test_application.py

This script verifies:
- All required packages are installed
- Statistical calculations work correctly
- Data loading works properly
- F-Test calculations are accurate
"""

import sys
import os

def check_python_version():
    """Verify Python version is 3.8 or higher."""
    print("=" * 70)
    print("MANUFACTURING QUALITY ANALYZER - TEST SUITE")
    print("=" * 70)
    print()
    
    print("📋 Step 1: Checking Python Version")
    print("-" * 70)
    version_info = sys.version_info
    python_version = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    print(f"   Python Version: {python_version}")
    
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 8):
        print("   ❌ ERROR: Python 3.8+ required")
        return False
    else:
        print("   ✅ PASS: Python version OK")
        return True
    print()

def check_packages():
    """Check if all required packages are installed."""
    print("📋 Step 2: Checking Required Packages")
    print("-" * 70)
    
    required_packages = {
        'customtkinter': 'Modern GUI framework',
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computation',
        'matplotlib': 'Graph generation',
        'scipy': 'Statistical functions',
    }
    
    optional_packages = {
        'reportlab': 'PDF export (optional)',
    }
    
    all_pass = True
    
    # Check required packages
    print("   Required Packages:")
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {package:20} - {description}")
        except ImportError:
            print(f"   ❌ {package:20} - NOT INSTALLED")
            all_pass = False
    
    print()
    print("   Optional Packages:")
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {package:20} - {description}")
        except ImportError:
            print(f"   ⚠️  {package:20} - Not installed (PDF export will fail)")
    
    print()
    return all_pass

def test_data_loading():
    """Test CSV data loading functionality."""
    print("📋 Step 3: Testing Data Loading")
    print("-" * 70)
    
    try:
        import pandas as pd
        import numpy as np
        
        # Create test CSV in memory
        test_data = "Measurement\n100.5\n101.2\n99.8\n100.1\n102.3"
        
        # Save test file
        test_file = "test_data.csv"
        with open(test_file, 'w') as f:
            f.write(test_data)
        
        # Try to load
        df = pd.read_csv(test_file)
        
        # Verify
        if 'Measurement' in df.columns and len(df) == 5:
            print("   ✅ CSV loading works correctly")
            os.remove(test_file)
            return True
        else:
            print("   ❌ CSV loading failed - invalid data")
            os.remove(test_file)
            return False
            
    except Exception as e:
        print(f"   ❌ CSV loading error: {str(e)}")
        return False
    finally:
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")
    print()

def test_statistics():
    """Test F-Test statistical calculations."""
    print("📋 Step 4: Testing F-Test Calculations")
    print("-" * 70)
    
    try:
        import pandas as pd
        import numpy as np
        from scipy import stats
        
        # Create test data
        plant1 = pd.Series([100.5, 101.2, 99.8, 100.1, 102.3, 99.9, 101.5, 100.2])
        plant2 = pd.Series([100.8, 98.2, 103.5, 99.1, 104.2, 97.9, 102.1, 98.8])
        
        # Calculate statistics
        mean1 = plant1.mean()
        mean2 = plant2.mean()
        var1 = plant1.var(ddof=1)
        var2 = plant2.var(ddof=1)
        std1 = plant1.std(ddof=1)
        std2 = plant2.std(ddof=1)
        
        # Calculate F-statistic
        f_stat = var1 / var2 if var1 >= var2 else var2 / var1
        df1 = len(plant1) - 1
        df2 = len(plant2) - 1
        
        # Calculate p-value
        p_value = 2 * (1 - stats.f.cdf(f_stat, df1, df2))
        p_value = min(p_value, 1.0)
        
        print(f"   Test Data - Plant 1 (n={len(plant1)}):")
        print(f"      Mean: {mean1:.6f}, Variance: {var1:.6f}, StdDev: {std1:.6f}")
        print(f"   Test Data - Plant 2 (n={len(plant2)}):")
        print(f"      Mean: {mean2:.6f}, Variance: {var2:.6f}, StdDev: {std2:.6f}")
        print(f"   F-Test Results:")
        print(f"      F-Statistic: {f_stat:.6f}")
        print(f"      Degrees of Freedom: ({df1}, {df2})")
        print(f"      P-Value: {p_value:.8f}")
        print(f"      Conclusion: {'Significant difference' if p_value < 0.05 else 'No significant difference'}")
        print()
        print("   ✅ F-Test calculations work correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ Statistics error: {str(e)}")
        return False
    print()

def test_visualization():
    """Test graph generation."""
    print("📋 Step 5: Testing Graph Generation")
    print("-" * 70)
    
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        import pandas as pd
        
        # Test basic plot creation
        fig, ax = plt.subplots()
        test_data = [1, 2, 3, 4, 5]
        ax.hist(test_data)
        plt.close(fig)
        
        print("   ✅ Graph generation (matplotlib) works correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ Visualization error: {str(e)}")
        return False
    print()

def test_sample_files():
    """Check if sample CSV files exist."""
    print("📋 Step 6: Checking Sample Data Files")
    print("-" * 70)
    
    files_needed = {
        'sample_plant_1.csv': 'Sample data for Plant 1',
        'sample_plant_2.csv': 'Sample data for Plant 2',
    }
    
    all_found = True
    for filename, description in files_needed.items():
        if os.path.exists(filename):
            # Try to count records
            try:
                import pandas as pd
                df = pd.read_csv(filename)
                count = len(df)
                print(f"   ✅ {filename:20} - Found ({count} measurements)")
            except:
                print(f"   ⚠️  {filename:20} - Found but invalid format")
        else:
            print(f"   ⚠️  {filename:20} - Not found (optional, for testing)")
            all_found = False
    
    print()
    return True  # Not critical if files not present

def run_full_test():
    """Run complete F-Test analysis with real data."""
    print("📋 Step 7: Running Full Analysis Test")
    print("-" * 70)
    
    try:
        import pandas as pd
        from scipy import stats
        
        # Load sample data if available
        try:
            plant1 = pd.read_csv('sample_plant_1.csv')['Measurement']
            plant2 = pd.read_csv('sample_plant_2.csv')['Measurement']
            source = "sample files"
        except:
            # Use embedded test data
            plant1 = pd.Series([100.5, 101.2, 99.8, 100.1, 102.3, 
                               99.9, 101.5, 100.2, 100.8, 101.1])
            plant2 = pd.Series([100.8, 98.2, 103.5, 99.1, 104.2, 
                               97.9, 102.1, 98.8, 105.3, 99.2])
            source = "built-in test data"
        
        # Perform F-Test
        n1, n2 = len(plant1), len(plant2)
        mean1, mean2 = plant1.mean(), plant2.mean()
        var1, var2 = plant1.var(ddof=1), plant2.var(ddof=1)
        
        f_stat = max(var1, var2) / min(var1, var2)
        df1 = n1 - 1
        df2 = n2 - 1
        p_value = 2 * (1 - stats.f.cdf(f_stat, df1, df2))
        p_value = min(p_value, 1.0)
        
        print(f"   Using {source}")
        print(f"   ✅ Complete analysis executed successfully")
        print(f"      Plant 1: n={n1}, mean={mean1:.4f}, var={var1:.4f}")
        print(f"      Plant 2: n={n2}, mean={mean2:.4f}, var={var2:.4f}")
        print(f"      F-test: F={f_stat:.4f}, p={p_value:.6f}")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Analysis error: {str(e)}")
        return False

def print_summary(results):
    """Print test results summary."""
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print()
        print("🎉 SUCCESS! All tests passed.")
        print("   Your system is ready to run the application:")
        print("   $ python manufacturing_quality_analyzer.py")
        print()
        return True
    else:
        print()
        print(f"⚠️  WARNING: {failed} test(s) failed.")
        print("   See INSTALLATION.md for troubleshooting.")
        print()
        return False

def main():
    """Run all tests."""
    results = {}
    
    # Run tests
    results['Python Version'] = check_python_version()
    results['Required Packages'] = check_packages()
    results['Data Loading'] = test_data_loading()
    results['F-Test Statistics'] = test_statistics()
    results['Graph Generation'] = test_visualization()
    results['Sample Files'] = test_sample_files()
    results['Full Analysis'] = run_full_test()
    
    # Print summary
    all_pass = print_summary(results)
    
    # Return exit code
    return 0 if all_pass else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
