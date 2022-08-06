## Generating nginx.conf

```sh
# Go to template folder
cd template

# Run the script
python template.py    

# Replace the old file with the new generated one
cp generated_nginx.conf ../nginx.conf

# Restart nginx container
cd ..
docker-compose restart
```