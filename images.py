import os
import re
import shutil

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"C:\Users\krash\Documents\lrjsec-blog\content\posts"
attachments_dir = r"C:\Users\krash\Documents\obsidian\Knowledge-Management\KM4OS\TemplateVault\Attachments"
static_images_dir = r"C:\Users\krash\Documents\lrjsec-blog\static\images"

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Step 2: Find all image links in the format ![Image Description](/images/filename.png)
        images = re.findall(r'!\[([^]]*)\]\(([^)]*\.png)\)', content)

        # Step 3: Replace image links and ensure URLs are correctly formatted
        for alt_text, image_filename in images:
            image_source = os.path.join(attachments_dir, image_filename)
            if os.path.exists(image_source):
                # Copy image to Hugo's static/images directory
                destination_path = os.path.join(static_images_dir, image_filename)
                shutil.copy(image_source, destination_path)
                print(f"Copied {image_filename} to {destination_path}")

                # Prepare the Markdown-compatible link with correct path
                markdown_image = f"![{alt_text}](/images/{image_filename})"

                # Replace the original Markdown image link
                content = content.replace(f"![{alt_text}]({image_filename})", markdown_image)
            else:
                print(f"Image {image_filename} not found in {attachments_dir}")

        # Step 4: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")