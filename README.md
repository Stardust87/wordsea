<h1 align="center">
  <a href="https://wordsea.xyz/" target="_blank">
    <picture>
      <img src="assets/logo.png" alt="WordSea logo" width="120" height="120" />
    </picture>
  </a>
<p align="center">WordSea</p>
</h1>

<h2 align="center">
  Let written be seen
</h2>

WordSea is a SvelteKit web application designed to help memorize new English words. You can check it on [wordsea.xyz](https://wordsea.xyz/).

 Core idea is to discover words in a mnemonic way by associating words with their definition-based visualizations.
 
 Only small subset of words has clear visual representation (e.g. apple, parachute), so the rest (e.g. imagine, eon) need to be tackled differently. 

## Setup

### Prerequisites

- [Docker](https://www.docker.com/)
- [Node.js](https://nodejs.org/en/)

Start by cloning the repository
```bash
git clone https://github.com/Stardust87/wordsea
cd wordsea
```

### Application
```bash
cd app
npm install
cd ..
docker compose up
```

### Database

Data is stored in MongoDB and its dump is available for download [here](https://mega.nz/file/h8k00b7J#xAdZlAQeWzNCLwL1hFfKhafU2sbZCrLgHaaf8D1CnJg).

Check the container id and restore the dump 
```bash
docker exec -i [container_id] mongorestore --gzip --nsInclude="wordsea.*" --archive < [dump_path]
```


## Word cards

<h2 >
    <picture>
      <img src="assets/slapdash.jpg" alt="slapdash meaning"/>
    </picture>
</h2>
<h2 >
    <picture>
      <img src="assets/amenity.jpg" alt="amenity meaning"  />
    </picture>
</h2>

## Roadmap

## Support
