FROM node:12

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package.json .
COPY package-*.json .

RUN npm install -g @angular/cli
RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

EXPOSE 80
EXPOSE 443
CMD ng build && ng serve --port 80 --host 0.0.0.0 --proxy-config proxy.conf.json --disable-host-check
