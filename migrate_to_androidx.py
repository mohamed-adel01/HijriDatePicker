import os
import re
from datetime import datetime

# Mapping of old to new imports
ANDROIDX_MAPPING = {
    'android.support.v4.app': 'androidx.core.app',
    'android.support.v4.content': 'androidx.core.content',
    'android.support.v4.view': 'androidx.core.view',
    'android.support.v4.widget': 'androidx.core.widget',
    'android.support.v4.util': 'androidx.core.util',
    'android.support.v7.app': 'androidx.appcompat.app',
    'android.support.v7.widget': 'androidx.appcompat.widget',
    'android.support.design': 'com.google.android.material',
    'android.support.constraint': 'androidx.constraintlayout',
    'android.support.v4.view.ViewPager': 'androidx.viewpager.widget.ViewPager',
    'android.support.v4.app.FragmentPagerAdapter': 'androidx.fragment.app.FragmentPagerAdapter',
    'android.support.v4.app.Fragment': 'androidx.fragment.app.Fragment',
    'android.support.v4.app.DialogFragment': 'androidx.fragment.app.DialogFragment',
    'android.support.v4.app.FragmentManager': 'androidx.fragment.app.FragmentManager',
    'android.support.v4.app.FragmentActivity': 'androidx.fragment.app.FragmentActivity',
    'android.support.v7.app.AppCompatActivity': 'androidx.appcompat.app.AppCompatActivity',
    'android.support.v7.app.ActionBar': 'androidx.appcompat.app.ActionBar',
    'android.support.v4.view.accessibility.AccessibilityNodeInfoCompat': 'androidx.core.view.accessibility.AccessibilityNodeInfoCompat'
}

def update_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        print(f"Skipping binary or non-text file: {file_path}")
        return False
    
    original_content = content
    modified = False

    # Update import statements
    for old_import, new_import in ANDROIDX_MAPPING.items():
        if old_import in content:
            content = content.replace(old_import, new_import)
            modified = True
    
    # Update gradle dependencies if it's a build.gradle file
    if file_path.endswith('build.gradle'):
        old_deps = [
            "implementation 'com.android.support:appcompat-v7:",
            "implementation 'com.android.support:support-v4:",
            "implementation 'com.android.support:design:",
            "implementation 'com.android.support.constraint:constraint-layout:"
        ]
        new_deps = [
            "implementation 'androidx.appcompat:appcompat:1.6.1'\n    implementation 'androidx.core:core-ktx:1.10.1'",
            "implementation 'androidx.legacy:legacy-support-v4:1.0.0'",
            "implementation 'com.google.android.material:material:1.9.0'",
            "implementation 'androidx.constraintlayout:constraintlayout:2.1.4'"
        ]
        
        for old_dep, new_dep in zip(old_deps, new_deps):
            if old_dep in content:
                # Replace the entire line containing the old dependency
                content = re.sub(f"{old_dep}.*\n", f"    {new_dep}\n", content)
                modified = True

    # Only write back if changes were made
    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated: {file_path}")
        return True
    return False

def process_directory(directory):
    files_modified = 0
    files_processed = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file.endswith(('.java', '.kt', '.gradle', '.xml')):
                file_path = os.path.join(root, file)
                files_processed += 1
                if update_file_content(file_path):
                    files_modified += 1
                
    return files_processed, files_modified

def main():
    print(f"Starting AndroidX migration script at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Created by: mohamed-adel01")
    
    # Get the directory where the script is running
    current_dir = os.getcwd()
    
    print(f"\nProcessing directory: {current_dir}")
    files_processed, files_modified = process_directory(current_dir)
    
    print(f"\nMigration completed!")
    print(f"Files processed: {files_processed}")
    print(f"Files modified: {files_modified}")

if __name__ == "__main__":
    main()
