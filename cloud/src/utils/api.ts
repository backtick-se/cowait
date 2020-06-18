export async function callApi<T>(method: string, url: string, data?: any): Promise<T | null> {
  const request = {
    method,
    headers: {
      Accept: 'application/json'
    },
    body: JSON.stringify(data)
  }

  const response = await fetch(url, request)
  if (!response.ok) throw new Error(response.statusText)

  const responseData = await (response.json() as Promise<{ data: T}>)

  return responseData ? responseData.data : null
}