# Kit-API

An API dedicated to kitty cats.

## What is Kit-API

Kit-API is a project I started when another cat fact API that I used for a while went down for a
few days. Hopefully Kit-API can provide cat facts to someone else in their time of need. The API
is completely free to use, and open source.

## Public Endpoints

All endpoints should be prefixed with `https://kit-api.com/v1`.

 - `/fact`: Gets 1 random fact.
 - `/fact/{id}`: Gets a fact with a particular id. e.g `/fact/2`
 - `/system/requests`: Gets the total requests made on the current API version.

## Utilizing Kit-API

To get started just make a request to one of the endpoints!

---

### Getting a random fact using Bash + cURL.
```bash
curl -X GET "https://kit-api.com/v1/fact"
```
##### Response
> {"id": 11, "fact": "Cats have 18 toes.", "uses": 30}

---

### Getting a fact by ID in Python asynchronously.

```python
import aiohttp
import asyncio

async def main() -> None:
    URL = "https://kit-api.com/v1/fact/12"
    session = aiohttp.ClientSession()

    async with session.get(URL) as response:
        print(await response.json())

    await session.close()

if __name__ == "__main__"
    asyncio.run(main())
```
##### Response
> {"id": 12,"fact": "Cat owners spend around 2 Billion USD per year on cat food.", "uses": 25}

---

### Getting the total number of requests in Rust asynchronously.
```rs
use tokio;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let url = "https://kit-api.com/v1/system/requests";

    let response = reqwest::get(url).await?;
    println!("{}", response.text().await?);

    Ok(())
}
```
##### Response
> 123

---

## License

Kit-API is licensed under the [BSD 3-Clause License](https://github.com/Jonxslays/kit-api/blob/master/LICENSE).
